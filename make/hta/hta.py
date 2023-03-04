import os, sys
from base64 import b64encode
from jinja2 import Template

from model import *
from helpers import *


@DataTracker
def makeHtaFromCmdByJscriptWscript(cmdline: str) -> AceStr:
    """Returns a HTA file which will execute cmdline"""
    cmdline = cmdline.replace('\r', '')
    cmdline = cmdline.replace('\n', '')

    hta = renderTemplate(
        'make/hta/hta-jscript-exec.hta',
        data=cmdline
    )
    return AceStr(hta)
