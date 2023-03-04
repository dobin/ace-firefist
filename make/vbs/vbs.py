import os, sys
from base64 import b64encode
from jinja2 import Template
import logging

from model import *
from helpers import getTemplate

logger = logging.getLogger('basic_logger')


@DataTracker
def makeVbsFromCmdByWscript(cmdline: str, disableQuoting=False) -> AceStr:
    """Return VBS file executing cmdline (with Wscript.Shell)"""
    template = getTemplate('make/vbs/wscriptshell-cmdline.vbs')

    cmdline = cmdline.replace('\r', '')
    cmdline = cmdline.replace('\n', '')
    if '"' in cmdline and not disableQuoting:
        logger.warn("Note: Replacing {} \" with \"\" in input".format(cmdline.count('"')))
        # double commandline quotes
        cmdline = cmdline.replace('"', '""')

    rendered = template.render(
        cmdline=cmdline
    )
    return AceStr(rendered)
