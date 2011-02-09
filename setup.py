# from ez_setup import use_setuptools
# use_setuptools()
from setuptools import setup, find_packages
from datapkg import __version__, __license__, __description__, __description_long__

setup(
    name='datapkg',
    version=__version__,
    # metadata
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    license=__license__,
    description=__description__,
    long_description=__description_long__,
    keywords='data, packaging, component, tool',
    url='http://okfn.org/projects/datapkg',
    classifiers=[
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools>=0.6c',
        # make ckan support obligatory for time being
        'ckanclient>=0.3',
    ],
    entry_points='''
    [distutils.setup_keywords]
    datapkg_index=datapkg.pypkgtools:datapkg_index

    [egg_info.writers]
    datapkg_index.txt=setuptools.command.egg_info:write_arg
    
    [console_scripts]
    datapkg=datapkg.cli:main

    [datapkg.cli]
    help = datapkg.cli:HelpCommand
    about = datapkg.cli.standard:AboutCommand
    license = datapkg.cli.standard:LicenseCommand
    man = datapkg.cli.standard:ManCommand
    list = datapkg.cli.standard:ListCommand
    search = datapkg.cli.standard:SearchCommand
    info = datapkg.cli.standard:InfoCommand
    dump = datapkg.cli.standard:DumpCommand
    init = datapkg.cli.standard:InitCommand
    create = datapkg.cli.standard:CreateCommand
    register = datapkg.cli.standard:RegisterCommand
    update = datapkg.cli.standard:UpdateCommand
    install = datapkg.cli.download:DownloadCommand
    upload = datapkg.cli.upload:UploadCommand

    [datapkg.index]
    simple = datapkg.index.base:SimpleIndex
    file = datapkg.index.base:FileIndex
    ckan = datapkg.index.ckan:CkanIndex
    db = datapkg.index.db:DbIndexSqlite
    egg = datapkg.index.egg:EggIndex

    [datapkg.distribution]
    json = datapkg.distribution:JsonDistribution
    python = datapkg.distribution:PythonDistribution

    [datapkg.resource_downloader]
    simple = datapkg.download:ResourceDownloaderSimple 
    ''',
    test_suite='nose.collector',
    zip_safe=False,
)
