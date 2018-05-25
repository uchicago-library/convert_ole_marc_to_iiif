# convert_ole_marc_to_iiif

A CLI application to take exported MARC XML records and convert them to IIIF

## Prerequisites

- marc2iiif
- pyiiif

## Quickstart

```bash
$ git clone git@github.com:uchicago-library/convert_ole_marc_to_iiif
$ cd convert_ole_marc_to_iiif
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python setup.py install
$ convert_record --metadata-only -o foo.iiif [path to a OLE exported MARC record]
```

Following these instructions will install the tool to a virtual environment on your system and conver the XML record to IIIF and save it to a file named 'foo.iiif' in your current working directory.

However, if you want to create a full IIIF record taht includes a sequence with canvases for a set of IIIF images you need to do something like the below example.

```bash
$ git clone git@github.com:uchicago-library/convert_ole_marc_to_iiif
$ cd convert_ole_marc_to_iiif
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python setup.py install
$ convert_record --image-manifest my_manifest.txt --metadata-only -o foo.iiif [path to a OLE exported MARC record]
```

Following the example above the tool will generate a full IIIF record with a sequence containing canvases for each IIIF image list in the file 'my_manifest.txt'.

## How to write the manifest list file

The manifest file should be a plain text file with a line per each IIIF image that you want to include in the exported IIIF record. The images should be listed in the order in which you want them displayed in the IIIF record. 

The URLS should be valid IIIF image identification URLS like so:

- https://my.iiif.server/my_iiif_image_identifer_1/info.json

The images should not be URLS to IIIF display images so they should not look like:

- https://iiif-server.lib.uchicago.edu/mvol/0004/1939/0330/TIFF/mvol-0004-1939-0330_0239.tif/full/full/0/default.jpg

## Author

- verbalhanglider <tdanstrom@uchicago.edu>
