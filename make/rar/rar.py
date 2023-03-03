import argparse
import io
import os, sys
from typing import List
import tempfile

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from lib.librar import archive


@DataTracker
def makeRar(files: List[AceFile], password=None) -> AceBytes:
    if len(files) == 0:
        raise Exception("No files given for rar")

    with tempfile.TemporaryDirectory() as directory:
        outFile = os.path.join(directory, "archive.rar")
        fsFiles = []

        # create all AceFiles
        for aceFile in files:
            file = os.path.join(directory, aceFile.name)
            with open(file, "wb") as f:
                f.write(aceFile.data)
                fsFiles.append(file)

        # Create rar file
        a = archive.Archive(outFile, base_path='.')
        # a.use_syslog()
        for fsFile in fsFiles:
            a.add_file(fsFile)

        if password is not None:
            a.set_password(password)
        a.set_exclude_base_dir(True)
        a.run()

        # read rar file again
        with open(outFile, "rb") as f:
            rarData = f.read()

    return AceBytes(rarData)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rar_name', help='')
    parser.add_argument('--file_name', help='')
    parser.add_argument('--file_data', help='')
    args = parser.parse_args()

    file = AceFile(args.file_name, bytes(args.file_data, 'utf-8'))
    rarData = makeRar(
        [file],
    )

    f = open(args.rar_name, 'wb')
    f.write(rarData)
    f.close()


if __name__ == "__main__":
    main()
