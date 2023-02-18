import argparse
import io
import os, sys
from typing import List

import zipfile

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *


@PluginDecorator
def makeZip(files: List[AceFile]) -> AceBytes:
    zipData = io.BytesIO()

    with zipfile.ZipFile(zipData, "a",
                        zipfile.ZIP_DEFLATED, False) as zip_file:
        
        for file in files:
            zip_file.writestr(file.name, file.data)

    return AceBytes(zipData.getvalue())


def main():
    # python3 -m make.iso.iso --iso-name new.iso --file_name test.txt --file_data 'testing'
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
