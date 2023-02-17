import os, sys

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from model import AceFile, PluginDecorator


@PluginDecorator
def makePowershell(input: str, options) -> str:
    ret = "{}".format(input)
    return ret

