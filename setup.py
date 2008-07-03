# from ez_setup import use_setuptools
# use_setuptools()
from setuptools import setup, find_packages
from datapkg import __version__, __license__, __description__

setup(
    name='datapkg',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools>=0.6c',
        'PasteDeploy>=1.0', 'PasteScript>=1.0',
        'SQLAlchemy>=0.4',
    ],
    entry_points='''
    [paste.paster_create_template]
    datapkg=datapkg:DataPkgTemplate
    
    [console_scripts]
    datapkg=datapkg.cli:main
    ''',

    # metadata
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    license=__license__,
    description=__description__,
    keywords='data packaging component tool',
    url='http://www.okfn.org/',
    classifiers=[
    ],
)
