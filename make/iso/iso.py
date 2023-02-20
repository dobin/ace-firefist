import argparse
import io
import os, sys
from typing import List
import pycdlib

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *


@DataTracker
def makeIso(files: List[AceFile]) -> AceBytes:
    # https://clalancette.github.io/pycdlib/example-creating-joliet-iso.html
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)
    for file in files:
        filename = "/{};1".format(file.name.upper())
        filenameJoliet = "/{}".format(file.name)
        iso.add_fp(io.BytesIO(file.data), len(file.data), filename, joliet_path=filenameJoliet)

    isoFileData = io.BytesIO()    
    iso._write_fp(isoFileData, 32768, None, None)
    iso.close()

    return AceBytes(isoFileData.getvalue())


def main():
    # python3 -m make.iso.iso --iso_name new.iso --file_name test.txt --file_data 'testing'
    parser = argparse.ArgumentParser()
    parser.add_argument('--iso_name', help='')
    parser.add_argument('--file_name', help='')
    parser.add_argument('--file_data', help='')
    args = parser.parse_args()

    file = AceFile(args.file_name, bytes(args.file_data, 'utf-8'))
    isoData = makeIso(
        [file],
    )

    f = open(args.iso_name, 'wb')
    f.write(isoData)
    f.close()


if __name__ == "__main__":
    main()
