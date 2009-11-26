from setuptools import setup, find_packages

setup(
    name='datapkgdemo',
    version="0.1",
    license="MIT",
    description="A demonstration datapkg containing the poem The Windhover",
    author="Open Knowledge Foundation",
    author_email="info@okfn.org",
    url='http://ckan.net/package/datapkgdemo',
    download_url='http://knowledgeforge.net/ckan/datapkgdemo-0.1.tar.gz',

    ## IGNORE THIS
    # information about what to include
    packages=find_packages(),
    include_package_data=True,
)
