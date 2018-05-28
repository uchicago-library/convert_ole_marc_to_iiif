from argparse import ArgumentParser, Action, ArgumentError
from os.path import exists
import requests

__version__ = "0.0.1"
__author__ = "Tyler Danstrom"

class ExtractIIIFImageLinks(Action):
    """a custom action class to process the manifest.txt file list of IIIF links, check them for validity and reutrn a list of the links
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(ExtractIIIFImageLinks, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, args, values, options_string=None):
        if not exists(values):
            raise ArgumentError(self, "value for --image-manifest does not exist on disk")
        imgs = []
        with open(values, 'r', ) as read_file:
            lines = read_file.readlines()
            for line in lines:
                if not requests.get(line, 'head').status_code == 200:
                    msg = "{} in {} is not a valid IIIF image url".format(line, dest)
                    raise ArgumentError(self, msg)
                else:       
                    imgs.append(line)
        setattr(args, self.dest, imgs)


def main():
    try:
        arguments = ArgumentParser(description="A tool to take an OLE exported MARC XML record and convert it to IIIF")
        record_arg = arguments.add_argument('record', type=str, action='store', help="The path to the XML record that you want to convert to IIIF")
        incl_imgs_args = arguments.add_argument("--include-images", action='store_true', help="An optional field to indicate whether to include a Sequence with images in outputted record. Default is False.", default=False)
        img_manifest_arg = arguments.add_argument("--image-manifest", type=str, action='store', help="A plain text file containing a list of IIIF image links to include in the IIIF outputted record")
        parsed_args = arguments.parse_args()
        if parsed_args.include_images and not parsed_args.image_manifest:
            raise ArgumentError(incl_imgs_args, "If you want to include images you must also define the image-manifest argument")
        print(parsed_args)
        return 0
    except KeyboardInterrupt:
        return 131
