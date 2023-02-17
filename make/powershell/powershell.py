import os, sys

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import lib.pylnk3.helpers
from model import AceFile, PluginDecorator, disableOut


@PluginDecorator
def makePowershell(input: str, options) -> bytes:
    ret = "{}".format(input)

    return bytes(ret, 'utf-8')

