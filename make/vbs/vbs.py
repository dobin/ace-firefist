import os, sys
from base64 import b64encode
from jinja2 import Template

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from model import AceFile, PluginDecorator


@PluginDecorator
def makeVbsExecEncPs1(data: str) -> str:
    templateFile = 'exec-enc-powershell.vbs'

    data = data.replace('\r', '')
    data = data.replace('\n', '')
    with open('make/vbs/' + templateFile) as f:
        template = Template(f.read())
    renderedHtml = template.render(
        data=data
    )
    return renderedHtml
