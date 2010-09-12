'''Pluggable uploaders to upload material to storage.

We use the OFS library for talking to backends and this module is just a think
wrapper around that.

We specify where material is uploaded to using a 'upload spec'
(upload-spec), which are of the form::

    {upload-dest-id}://BUCKET/LABEL

For example::

    ## default ckan upload
    ckan://BUCKET/LABEL

    ## an s3 upload destination
    my-s3://BUCKET/LABEL

    ## local pairtree
    my-pairtree://BUCKET/LABEL

    ## google storage
    my-google-storage://BUCKET/LABEL

Upload destinations are specified in your datapkg config file and are of the form::

    [upload:dest-id]
    ofs.backend = {s3|google|archive.org|...}
    ## see OFS documentation for a given back
    {config-option} = {config-value}
'''
import datapkg
import pkg_resources

class Uploader(object):
    def __init__(self, verbose=False):
        self.verbose = True

    def upload(self, filepath, uploadspec):
        backend = self.load_ofs_backend(uploadspec)
        bucket,label = self.get_bucket_label(uploadspec)
        backend.put_stream(bucket, label, open(filepath))

    def load_ofs_backend(self, uploadspec):
        uploadid = uploadspec.split(':')[0]
        configsection = 'upload:%s' % uploadid
        uploadinfo = dict(datapkg.CONFIG.items(configsection))
        ofs_type = uploadinfo['ofs.backend']
        backend = None
        for entry_point in pkg_resources.iter_entry_points('ofs.backend'):
            if ofs_type == entry_point.name:
                backend_cls = entry_point.load()
        if backend_cls == None:
            msg = 'No suitable OFS backend for uploading found'
            raise Exception(msg)
        uploadconfig = dict(uploadinfo)
        del uploadconfig['ofs.backend']
        backend = backend_cls(**uploadconfig)
        return backend

    def get_bucket_label(self, uploadspec):
        bucket_label = uploadspec.split('://')[1]
        parts  = bucket_label.split('/')
        bucket = parts[0]
        label = '/'.join(parts[1:])
        return bucket,label

