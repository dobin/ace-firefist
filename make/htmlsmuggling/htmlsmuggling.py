import argparse
from jinja2 import Template
from pathlib import Path
from base64 import b64encode
from pathlib import Path
import os
import sys

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import getTemplate


@DataTracker
def makeHtmlSmuggling(file: AceFile) -> AceStr:
    """Make a HTML site from template from which the file can be downloaded"""
    templateFile = 'autodownload.html'
    template = getTemplate('make/htmlsmuggling/', templateFile)
    
    # Arguments for the template:
    # - data: is file base64 encoded
    # - filename: the filename
    data = b64encode(file.data).decode()
    renderedHtml = template.render(
        data=data,
        filename=file.name,
    )
    return AceStr(renderedHtml)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="")
    parser.add_argument("--payload_data", help="")
    parser.add_argument("--payload_name", help="")
    args = parser.parse_args()

    file = AceFile(
        args.payload_name,
        bytes(args.payload_data, 'utf-8')
    )
    htmlData = makeHtmlSmuggling(file)

    f = open(args.filename, 'w')
    f.write(htmlData)
    f.close()


if __name__ == "__main__":
    main()