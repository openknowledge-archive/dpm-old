'''Pluggable uploaders to upload material to storage.

We use the OFS library for talking to backends and this module is just a think
wrapper around that.
'''
import dpm
import pkg_resources

class Uploader(object):
    '''Handle uploading to storage backends using OFS.'''

    def __init__(self, verbose=False):
        self.verbose = True

    def upload(self, fileobj, upload_spec):
        '''Upload contents of `fileobj` to location specified by `upload_spec`.

        :param upload_spec: an upload spec see documentation for upload
        command.
        '''
        backend = self.load_ofs_backend(upload_spec)
        bucket,label = self.get_bucket_label(upload_spec)
        backend.put_stream(bucket, label, fileobj)

    def load_ofs_backend(self, uploadspec):
        uploadid = uploadspec.split(':')[0]
        configsection = 'upload:%s' % uploadid
        uploadinfo = dict(dpm.CONFIG.items(configsection))
        ofs_type = uploadinfo['ofs.backend']
        backend_cls = None
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

