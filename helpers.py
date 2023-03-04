from typing import List
import logging
from base64 import b64encode

from model import *
import config
from utilities import *

logger = logging.getLogger('basic_logger')


@DataTracker
def base64encode(input: AceBytes) -> AceStr:
    data = b64encode(input).decode()
    return AceStr(data)


@DataTracker
def renderTemplate(path: str, **kwargs) -> AceStr:
    template = getTemplate(path)
    rendered = template.render(kwargs)
    return AceStr(rendered)


@DataTracker
def readFileContent(filename: str) -> AceBytes:
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return AceBytes(data)


@DataTracker
def readFileContentStr(filename: str) -> AceBytes:
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return AceStr(data)


@DataTracker
def makeAceFile(name: str, data: bytes) -> AceFile:
    aceFile = AceFile(name, data)
    if config.ENABLE_SCANNING is not None:
        scanAv(aceFile)
    return aceFile
