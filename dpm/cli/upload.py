import os

from dpm.cli.base import Command
import dpm.upload


class UploadCommand(Command):
    name = 'upload'
    summary = 'Upload a resource or package to a storage system'
    min_args = 2
    max_args = 2
    usage = \
'''%prog {path} {upload-spec}

Upload a file or package at {path} to {upload-spec}. Upload-spec are of the form::

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

Upload destinations are specified in your dpm config file and are of the form::

    [upload:dest-id]
    ofs.backend = {s3|google|archive.org|...}
    ## see OFS documentation for a given backend
    {config-option} = {config-value}
    '''

    def run(self, options, args):
        path = args[0]
        # is path a package or not?
        upload_spec = args[1]
        uploader = dpm.upload.Uploader(verbose=True)
        print 'Uploading, please be patient ...'
        uploader.upload(open(path), upload_spec)

