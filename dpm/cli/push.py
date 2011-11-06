import os
import logging
from ConfigParser import SafeConfigParser
import mimetypes
import csv
import urllib2
import urllib
import urlparse
import json
from dpm.cli.base import Command
from dpm.package import Package

logger = logging.getLogger('dpm.cli')

webstorable_mimetypes = ['text/csv']

class PushCommand(Command):
    name = 'push'
    summary = 'Push a package to a repository'
    min_args = 0
    max_args = 2
    usage = \
'''%prog [source-file webstore-url]

Push local package in current directory to remote repository specified in
.dpm/config. Alternatively push a single file to the webstore.

Examples:

    dpm push data/data.csv http://{api-key}@webstore.org/me/mydatabase/data?unique=Date
    dpm push
'''
    
    def run(self, options, args):
        if args:
            assert len(args) == 2, '2 arguments are needed'
            push_file(args[0], args[1])
        else:
            push_all()

def push_all():
    current_dir = os.path.abspath('.')
    pkg = Package.load(current_dir)
    # load .dpm/config and
    cfgpath = os.path.join(current_dir, '.dpm/config')
    if not os.path.exists(cfgpath):
        msg = 'No .dpm/config file found. push only works with source packages.'
        logger.error(msg)
        raise Exception(msg)
    cfg = SafeConfigParser() 
    cfg.read(cfgpath)
    # get remote URL
    remote_url = cfg.get('remote', 'url')
    remote_url = remote_url.rstrip('/')
    remote_webstore_url = cfg.get('remote', 'webstore')
    
    for resource in pkg.resources:
        local_path = resource.get('local_path', '')
        if not local_path:
            continue
        mimetype = mimetypes.guess_type(local_path)[0]
        if mimetype not in webstorable_mimetypes:
            logger.info('Skipping %s as not webstorable' % local_path)
            continue
        # webstore_url = resource.get('webstore_url', '')
        fn = os.path.splitext(os.path.basename(local_path))[0]
        webstore_url = remote_webstore_url + '/' + fn
        push_file(local_path, webstore_url)

def push_file(path, webstore_url):
    mimetype = mimetypes.guess_type(path)[0]
    if mimetype not in webstorable_mimetypes:
        logger.info('Skipping %s as not webstorable' % path)
        return
    table = WebstoreTable(webstore_url)
    count = 0
    power = 0
    logger.info('Pushing %s to %s' % (path, webstore_url))
    for dict_ in csv.DictReader(open(path)):
        try:
            table.writerow(dict_)
            count += 1
            if count % 2**power == 0:
                logger.info('Processed %s rows' % count)
                power += 1
        except:
            logger.error(dict_)
            raise

class WebstoreTable(object):
    def __init__(self, url):
        parsed = urlparse.urlparse(url)
        newparsed = list(parsed)
        username = parsed.username
        if username:
            # get rid of username:password@ in netloc
            newparsed[1] = parsed.netloc.split('@')[1]
        self.url = urlparse.urlunparse(newparsed)
        authorization = self._authorization(username, parsed.password)
        self._headers = {}
        self._headers['Content-Type'] = 'application/json'
        self._headers['Accept'] = 'application/json'
        if authorization:
            self._headers['Authorization'] = authorization

    def _authorization(self, username, password):
        '''Get authorization field for authorization header.
        
        If password is None we assume username is in fact API key.
        '''
        if username and password:
            secret = username + ':' + password
            authorization = 'Basic ' + secret.encode('base64')
            return authorization
        elif username: # API key
            return username
        else:
            return ''

    def writerow(self, dict_, unique_columns=None):
        if unique_columns:
            query = '?' + urllib.urlencode([('unique', u) for u in unique_columns])
            url = self.url + query
        else:
            url = self.url
        data = json.dumps(dict_)
        req = urllib2.Request(url, data, self._headers)
        response = urllib2.urlopen(req)
        return response 

