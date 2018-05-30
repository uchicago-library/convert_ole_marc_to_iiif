from setuptools import setup, find_packages


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
    name="convertOLERecords2IIIF",
    description="A CLI application to take exported OLE MARC XML records and convert them to IIIF.",
    version="1.0.0",
    long_description=readme(),
    author="Tyler Danstrom",
    author_email="tdanstrom@uchicago.edu",
    packages=find_packages(
        exclude=[
        ]
    ),
    include_package_data=True,
    url='https://github.com/uchicago-library/convert_ole_marc_to_iiif',
    dependency_links = [
        'https://github.com/uchicago-library/marc_field_lookup/tarball/master#egg=marcFieldsLookup',
        'https://github.com/uchicago-library/marc2iiif/tarball/master#egg=marc2iiif',
   ],
    entry_points = {
        'console_scripts': [
            'convert_record=OLEConversion2IIIF.__main__:main'
        ]
    }
)