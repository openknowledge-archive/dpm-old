from paste.script.templates import Template, var

vars = [
    var('version', 'Version (like 0.1)', default='0.1'),
    var('description', 'Title or one-line description of the package'),
    var('url', 'URL of project/package homepage'),
    var('long_description', 'Notes such as a multi-line description (in markdown)'),
    var('keywords', 'Space-separated keywords/tags'),
    var('author', 'Author name'),
    var('author_email', 'Author email'),
    var('license_name', 'License name'),
    var('zip_safe', 'True/False: if the package can be distributed as a .zip file',
        default=False),
]

class DataPkgTemplate(Template):
    _template_dir = 'default_distribution'
    summary = 'DataPkg default distribution template'
    vars = vars

class DataPkgFlatTemplate(Template):
    _template_dir = 'flat_distribution'
    summary = 'DataPkg "flat" template'
    vars = vars

