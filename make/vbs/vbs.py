import os, sys
from base64 import b64encode
from jinja2 import Template

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *


@PluginDecorator
def makeVbsExecEncPs1(commandline: str) -> AceStr:
    templateFile = 'exec-enc-powershell.vbs'

    commandline = commandline.replace('\r', '')
    commandline = commandline.replace('\n', '')
    with open('make/vbs/' + templateFile) as f:
        template = Template(f.read())
    renderedHtml = template.render(
        data=commandline
    )
    return AceStr(renderedHtml)
