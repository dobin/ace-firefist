import os, sys
from base64 import b64encode
from jinja2 import Template

from model import *
from helpers import getTemplate


@DataTracker
def makeHtaFromCmdByJscriptWscript(cmdline: str) -> AceStr:
    """Returns a HTA file which will execute cmdline"""
    template = getTemplate('make/hta/hta-jscript-exec.hta')
    cmdline = cmdline.replace('\r', '')
    cmdline = cmdline.replace('\n', '')
    renderedHtml = template.render(
        data=cmdline
    )
    return AceStr(renderedHtml)
