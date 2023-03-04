import os, sys
from base64 import b64encode
from jinja2 import Template
import logging
from typing import List

from model import *


@DataTracker
def makeBatFromCmds(cmds: List[str]) -> AceStr:
    """Returns a bat file of input cmds (list entries separated by windows newlines)"""
    return AceStr('\r\n'.join(cmds))
