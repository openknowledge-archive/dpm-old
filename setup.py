# from ez_setup import use_setuptools
# use_setuptools()
from setuptools import setup, find_packages
from dpm import __version__, __license__, __description__
try:
    __description_long__ = open('README.rst').read()
except:
    __description_long__ = ''

setup(
    name='dpm',
    version=__version__,
    # metadata
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    license=__license__,
    description=__description__,
    long_description=__description_long__,
    keywords='data, packaging, component, tool',
    url='http://okfn.org/projects/dpm',
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
    [egg_info.writers]
    datapkg_index.txt=setuptools.command.egg_info:write_arg
    
    [console_scripts]
    dpm=dpm.cli:main

    [dpm.cli]
    help = dpm.cli:HelpCommand
    about = dpm.cli.standard:AboutCommand
    license = dpm.cli.standard:LicenseCommand
    man = dpm.cli.standard:ManCommand
    list = dpm.cli.standard:ListCommand
    search = dpm.cli.standard:SearchCommand
    info = dpm.cli.standard:InfoCommand
    dump = dpm.cli.standard:DumpCommand
    init = dpm.cli.standard:InitCommand
    setup = dpm.cli.standard:SetupCommand
    register = dpm.cli.standard:RegisterCommand
    update = dpm.cli.standard:UpdateCommand
    download = dpm.cli.download:DownloadCommand
    clone = dpm.cli.download:DownloadCommand
    upload = dpm.cli.upload:UploadCommand
    push = dpm.cli.push:PushCommand

    [dpm.index]
    simple = dpm.index.base:SimpleIndex
    file = dpm.index.base:FileIndex
    ckan = dpm.index.ckan:CkanIndex
    egg = dpm.index.egg:EggIndex

    [dpm.distribution]
    json = dpm.distribution:JsonDistribution

    [dpm.resource_downloader]
    simple = dpm.download:ResourceDownloaderSimple 
    ''',
    test_suite='nose.collector',
    zip_safe=False,
)
