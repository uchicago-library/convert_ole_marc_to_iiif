from argparse import ArgumentParser, Action, ArgumentError
from marclookup.lookup import MarcField
from os.path import exists
import requests
from xml.etree import ElementTree

__version__ = "0.0.1"
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
            for datafield in datafields:
                print(datafield.attrib["tag"])
        else:
            raise ArgumentError(self, "value passed for record does not exist on disk")


def main():
    try:
        arguments = ArgumentParser(description="A tool to take an OLE exported MARC XML record and convert it to IIIF")
        record_arg = arguments.add_argument('record', type=str, action=TransformOLEXMLRecord, help="The path to the XML record that you want to convert to IIIF")
        incl_imgs_args = arguments.add_argument("--include-images", action='store_true', help="An optional field to indicate whether to include a Sequence with images in outputted record. Default is False.", default=False)
        img_manifest_arg = arguments.add_argument("--image-manifest", type=str, action=ExtractIIIFImageLinks, help="A plain text file containing a list of IIIF image links to include in the IIIF outputted record")
        parsed_args = arguments.parse_args()
        if parsed_args.include_images and not parsed_args.image_manifest:
            raise ArgumentError(incl_imgs_args, "If you want to include images you must also define the image-manifest argument")
        print(parsed_args)
        return 0
    except KeyboardInterrupt:
        return 131
