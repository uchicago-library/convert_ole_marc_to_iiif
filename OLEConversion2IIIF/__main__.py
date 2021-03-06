from argparse import ArgumentParser, Action, ArgumentError
from collections import namedtuple
import json
from marc2iiif.classes import IIIFMetadataBoxFromMarc, IIIFMetadataField, IIIFDataExtractionFromMarc
from marclookup.lookup import MarcField
from os.path import exists
import requests
from sys import stdout
from urllib.parse import urlparse
from uuid import uuid4
from xml.etree import ElementTree

__version__ = "1.0.0"
__author__ = "Tyler Danstrom"

class ExtractIIIFImageLinks(Action):
    """a custom action class to process the manifest.txt file list of IIIF links, check them for validity and reutrn a list of the links
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(ExtractIIIFImageLinks, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, args, values, options_string=None):
        if not args.include_images:
            raise ArgumentError(self, "cannot read image-manifest without include-images flag")
        if not exists(values):
            raise ArgumentError(self, "value for --image-manifest does not exist on disk")
        imgs = []
        with open(values, 'r', ) as read_file:
            lines = read_file.readlines()
            for line in lines: 
                line = line.strip()
                if not requests.get(line, 'head').status_code == 200:
                    msg = "{} in {} is not a valid IIIF image url".format(line, values)
                    raise ArgumentError(self, msg)
                else:       
                    imgs.append(line)
        setattr(args, self.dest, imgs)

class TransformOLEXMLRecord(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(TransformOLEXMLRecord, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, args, values, options_string=None):
        if exists(values):
            xml_doc = ElementTree.parse(values)
            xml_root = xml_doc.getroot()
            datafields = xml_root.findall("datafield")
            metadata = []
            identifier = ""
            title = "unknown"
            description = "A Cultural Heritage Object from the University of Chicago Library"
            for datafield in datafields:
                new_field = MarcField(field=datafield.attrib["tag"].strip())
                valid_subfields = [x.code for x in new_field.subfields]
                real_subfields = datafield.findall("subfield")
                for r_sf in real_subfields:
                    if new_field.field == '245' and r_sf.attrib['code'] == 'a':
                        title = r_sf.text
                    if new_field.label and "electronic location" in new_field.label.lower():
                        fragment = urlparse(r_sf.text).path
                        if fragment[0] == '/':
                            fragment = fragment[1:]
                        identifier += fragment
                    if r_sf.attrib["code"] in valid_subfields:
                        field_label = new_field.label
                        subfield_label = [x.label for x in new_field.subfields if x.code == r_sf.attrib["code"]]
                        if subfield_label[0].lower() in field_label.lower():
                            label = field_label
                        else:
                            label = field_label + " " + subfield_label[0]
                        new_mfield = IIIFMetadataField(label, r_sf.text)
                        metadata.append(new_mfield)
            new_iiif_mdata_box = IIIFMetadataBoxFromMarc(title, description, identifier, metadata)
            new_iiif = IIIFDataExtractionFromMarc(new_iiif_mdata_box)
            setattr(args, self.dest, new_iiif.to_dict())
        else:
            raise ArgumentError(self, "value passed for record does not exist on disk")


def main():
    try:
        arguments = ArgumentParser(description="A tool to take an OLE exported MARC XML record and convert it to IIIF")
        arguments.add_argument('record', type=str, action=TransformOLEXMLRecord, help="The path to the XML record that you want to convert to IIIF")
        arguments.add_argument("-o", "--output", action='store', type=str, help="A filepath to save the output to. If not absolute it will save in your current working directory")
        parsed_args = arguments.parse_args()
        if parsed_args.output and not exists(parsed_args.output):
            json.dump(parsed_args.record, open(parsed_args.output, 'w', encoding="utf-8"), indent=4)
        else:
            stdout.write(json.dumps(parsed_args.record, indent=4))
        return 0
    except KeyboardInterrupt:
        return 131
