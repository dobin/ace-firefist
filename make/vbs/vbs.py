import os, sys
from base64 import b64encode
from jinja2 import Template

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import getTemplate


@DataTracker
def makeVbsExecEncPs1(commandline: str) -> AceStr:
    templateFile = 'exec-enc-powershell.vbs'
    template = getTemplate('make/vbs/', templateFile)
    commandline = commandline.replace('\r', '')
    commandline = commandline.replace('\n', '')
    renderedHtml = template.render(
        data=commandline
    )
    return AceStr(renderedHtml)
