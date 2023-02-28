import os, sys
from base64 import b64encode
from jinja2 import Template

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
