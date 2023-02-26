import os, sys
from base64 import b64encode
from jinja2 import Template
import logging

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import getTemplate


@DataTracker
def makeCmdToDllWithOdbc(dllPath: str):
    templateFile = 'odbcconf-loaddll.cmd'
    template = getTemplate('make/cmd/', templateFile)
    script = template.render(
        dllPath=dllPath
    )
    return AceStr(script)


@DataTracker
def makeCmdFileDownloadWithCurl(url: str, destinationFile: str = None):
    """create curl <url> commandline"""
    #  -k, --insecure           Allow insecure server connections
    if destinationFile is None:
        s = "curl -k \"{}\"".format(url)
    else:
        s = "curl -k \"{}\" -o \"{}\"".format(url, destinationFile)
    return AceStr(s)
