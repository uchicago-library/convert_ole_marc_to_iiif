from argparse import ArgumentParser

__version__ = "0.0.1"
__author__ = "Tyler Danstrom"

def main():
    try:
        arguments = ArgumentParser(description="A tool to take an OLE exported MARC XML record and convert it to IIIF")
        arguments.add_argument('record', type=str, action='store', help="The path to the XML record that you want to convert to IIIF")
        arguments.add_argument("--metadata-only", action='store_true', help="An optional field to flag whether to save full IIIF records with sequences or just save the metadata portion", default=False)
        arguments.add_argument("--image-manifest", type=str, action='store', help="A plain text file containing a list of IIIF image links to include in the IIIF outputted record")
        parsed_args = arguments.parse_args()

        return 0
    except KeyboardInterrupt:
        return 131
