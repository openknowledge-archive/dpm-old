# from ez_setup import use_setuptools
# use_setuptools()
from setuptools import setup, find_packages
from datapkg import __version__, __license__, __description__, __description_long__

setup(
    name='datapkg',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools>=0.6c',
        'PasteDeploy>=1.0',
        'PasteScript>=1.0',
        # 'SQLAlchemy>=0.4',
        # make ckan support obligatory for time being
        'ckanclient>=0.2',
        'pip>=0.6',
    ],
    entry_points='''
    [paste.paster_create_template]
    datapkg-default=datapkg.templates:DataPkgTemplate
    datapkg-flat=datapkg.templates:DataPkgFlatTemplate
    
    [console_scripts]
    datapkg=datapkg.cli:main
    ''',

    # metadata
    author='Open Knowledge Foundation, Appropriate Software Foundation',
    author_email='info@okfn.org',
    license=__license__,
    description=__description__,
    long_description=__description_long__,
    keywords='data packaging component tool',
    test_suite='nose.collector',
    url='http://www.okfn.org/datapkg',
    classifiers=[
    ],
)
