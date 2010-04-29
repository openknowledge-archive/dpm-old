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
    url='http://www.okfn.org/datapkg',
    classifiers=[
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools>=0.6c',
        'PasteDeploy>=1.0',
        'PasteScript>=1.0',
        # 'SQLAlchemy>=0.4',
        # make ckan support obligatory for time being
        'ckanclient==0.3',
        'urlgrabber>=3.0'
    ],
    entry_points='''
    [paste.paster_create_template]
    datapkg-default=datapkg.templates:DataPkgTemplate
    datapkg-flat=datapkg.templates:DataPkgFlatTemplate
    
    [console_scripts]
    datapkg=datapkg.cli:main
    ''',
    test_suite='nose.collector',
    zip_safe=False,
)
