import os, sys
from base64 import b64encode

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from model import AceFile, PluginDecorator

# Notes:
# Use powershell.exe argument '-noexit' for testing


@PluginDecorator
def makePowershellCommand(input: str, options) -> str:
    """For use with PowerShell -Command {}"""
    ret = "{}".format(input)
    return ret


def makePowershellEncodedCommand(input: str, options) -> str:
    """For use with PowerShell -EncodedCommand {}"""
    text = makePowershellCommand(input, options)
    # https://stackoverflow.com/questions/71642299/how-to-use-python-to-represent-the-powershell-tobase64string-function
    text = bytearray(text, 'utf-16-le')
    b64 = b64encode(text).decode() # bytearray to str
    return b64
