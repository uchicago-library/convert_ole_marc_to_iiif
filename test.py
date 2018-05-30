import csv
from os import scandir
import json

def find_tiff_files(path, pattern='None'):
    for n_thing in scandir(path):
        if n_thing.is_dir():
            yield from find_tiff_files(n_thing.path, pattern=pattern)
        elif n_thing.is_file() and n_thing.path.endswith(".tif") and pattern in n_thing.path:
            yield n_thing.path

if __name__ == "__main__":
    list_of_files = scandir("./socsciIIIFRecords")
    rows = []
    for n in list_of_files:
        data = json.load(open(n.path, "r", encoding="utf-8"))
        label = data["label"]
        identifier = data["@id"].split("/")[-1]
        a_row = [label, identifier]
        rows.append(a_row)

    rows = sorted(rows, key=lambda x: x[0])

    with open("./index.csv", "w", encoding="utf-8", newline="") as wf:
        the_writer = csv.writer(wf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for a_row in rows:
            the_writer.writerow(a_row) 

    for a_row in rows:
        identifier = a_row[1].strip()
        matching_tiffs = find_tiff_files("Z:\DC_Work_in_Progress\Maps", pattern=identifier)
        for n in matching_tiffs:
            print(n)