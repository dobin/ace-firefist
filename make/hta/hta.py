import os, sys
from base64 import b64encode
from jinja2 import Template

from model import *
from helpers import getTemplate


@DataTracker
def makeHtaFromCmdByJscriptWscript(commandline: str) -> AceStr:
    template = getTemplate('make/hta/hta-jscript-exec.hta')
    commandline = commandline.replace('\r', '')
    commandline = commandline.replace('\n', '')
    renderedHtml = template.render(
        data=commandline
    )
    return AceStr(renderedHtml)
