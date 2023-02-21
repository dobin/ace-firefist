import os, sys
from base64 import b64encode
from jinja2 import Template
import logging

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import getTemplate

logger = logging.getLogger('basic_logger')


@DataTracker
def makeVbsFromCmdByWscript(commandline: str, disableQuoting=False) -> AceStr:
    templateFile = 'exec-enc-powershell.vbs'
    template = getTemplate('make/vbs/', templateFile)
    commandline = commandline.replace('\r', '')
    commandline = commandline.replace('\n', '')
    if '"' in commandline and not disableQuoting:
        logger.warn("Note: Replacing all \" with \"\" in input")
        # double commandline quotes
        commandline = commandline.replace('"', '""')
    renderedHtml = template.render(
        data=commandline
    )
    return AceStr(renderedHtml)
