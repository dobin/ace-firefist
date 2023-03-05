import os, sys
from base64 import b64encode
from jinja2 import Template
import logging

from model import *
from helpers import *


@DataTracker
def makeVbsFromCmdByWscript(cmdline: str, disableQuoting=False) -> AceStr:
    """Return VBS file executing cmdline (with Wscript.Shell)"""
    cmdline = cmdline.replace('\r', '')
    cmdline = cmdline.replace('\n', '')
    if '"' in cmdline and not disableQuoting:
        logging.warn("Note: Replacing {} \" with \"\" in input".format(cmdline.count('"')))
        # double commandline quotes
        cmdline = cmdline.replace('"', '""')

    vbs = renderTemplate(
        'make/vbs/wscriptshell-cmdline.vbs',
        cmdline=cmdline
    )
    return AceStr(vbs)
