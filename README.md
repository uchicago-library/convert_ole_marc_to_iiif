# convert_ole_marc_to_iiif

A CLI application to take exported MARC XML records and convert them to IIIF

## Prerequisites

- [marc2iiif](https://github.com/uchicago-library/marc2iiif)
- [pyiiif](https://github.com/uchicago-library/pyiiif)

## Quickstart

```bash
$ git clone git@github.com:uchicago-library/convert_ole_marc_to_iiif
$ cd convert_ole_marc_to_iiif
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python setup.py install
$ convert_record -h
```

Following these instructions will install the tool to a virtual environment on your system and run the command-line application that you just installed.

## Examples

```bash
$ convert_record -o foo.json [path to an OLE eported MARC record]
```

Performing this action, you will convert a MARC XML record to a metadata-only IIIF record and save it to a file named ```foo.json``` in your current working directory.

## Author

- verbalhanglider <tdanstrom@uchicago.edu>
