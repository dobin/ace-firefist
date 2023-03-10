import argparse
import io
import os, sys
from typing import List
from zipencrypt import ZipFile

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *


@DataTracker
def makeZip(files: List[AceFile], password: str=None) -> AceBytes:
    """Return a ZIP file containting files"""
    zipData = io.BytesIO()

    with ZipFile(zipData, "a") as zip_file:
        for file in files:
            if password is None:
                zip_file.writestr(file.name, file.data)
            else:
                zip_file.writestr(file.name, file.data, pwd=password.encode())

    return AceBytes(zipData.getvalue())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--zip_name', help='')
    parser.add_argument('--file_name', help='')
    parser.add_argument('--file_data', help='')
    args = parser.parse_args()

    file = AceFile(args.file_name, bytes(args.file_data, 'utf-8'))
    isoData = makeZip(
        [file],
    )

    f = open(args.zip_name, 'wb')
    f.write(isoData)
    f.close()


if __name__ == "__main__":
    main()
