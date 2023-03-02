import os, sys
from base64 import b64encode
from jinja2 import Template
import logging
from typing import List
import argparse

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import getTemplate
from make.powershell.powershell import *


@DataTracker
def makePeExecCmd(input, type) -> AceBytes:
    if type == "dll-bat":
        template = 'payloads/execcmd.dll'
    elif type == "dll-c2":
        template = 'payloads/execc2cmd.dll'
    elif type == "exe-bat":
        template = 'payloads/execcmd.exe'
    elif type == "exe-c2":
        template = 'payloads/execc2cmd.exe'
    else:
        logging.error("Wrong type: {}".format(type))
        return
    
    placeholderLen = 800
    placeholder = b" " * placeholderLen
    exchange = input + " " * (placeholderLen - len(input))
    exchangeBytes = bytes(exchange, 'ascii')
    if len(placeholder) != len(exchangeBytes):
        logging.error("makeDllExecC2cmd: len not equal, something went wrong: {} {}".format(len(placeholder), len(exchangeBytes)))

    # open original onenote
    file = open(template, 'rb')
    data = file.read()
    file.close()

    if not placeholder in data:
        logging.error("Could not find placeHolder in template")
    # replace the placeholder in our bat file
    data = data.replace(placeholder, exchangeBytes)
    return AceBytes(data)

