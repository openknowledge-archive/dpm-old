import simplejson

class Metadata(dict):
    keys = [
       'name', 
       'title',
       'license',
       'url',
       'download_url',
       'notes',
       'tags',
       ]

    def __setattr__(self, name, value):
        if name in self.keys:
            self[name] = value
        else:
            super(Metadata, self).__setattr__(name)

    def __getattr__(self, name):
        if name in self.keys:
            return self[name]
        else:
            return super(Metadata, self).__getattribute__(name)
    
    def pprint(self):
        return simplejson.dumps(self, indent=2)

    def __str__(self):
        return simplejson.dumps(self)


class MetadataConverter(object):

    @classmethod
    def from_distutils(self, data):
        name = data.get_name()
        title = data.get_description()
        if title == 'UNKNOWN': title = ''
        url = data.get_url()
        if url == 'UNKNOWN': url = ''
        notes = data.get_long_description()
        if notes == 'UNKNOWN': notes = ''
        download_url = data.get_download_url()
        if download_url == 'UNKNOWN': download_url = ''
        tags = " ".join(data.get_keywords()).split(' ')
        pkg_metadata = {
            'name': name,
            'title': title,
            'url': url,
            'download_url': download_url,
            'notes': notes,
            'tags': tags,
        }
        return Metadata(pkg_metadata)

    @classmethod
    def to_distutils(self, metadata):
        distutils_metadata = distutils.dist.DistributionMetadata()
        for key, value in metadata.items():
            setkey = key
            tval = value
            if key == 'tags':
                setkey = 'keywords'
            elif key == 'title':
                setkey = 'description'
            elif key == 'notes':
                setkey = 'long_description'
            setattr(distutils_metadata, setkey, tval)
        return distutils_metadata


