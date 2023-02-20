import os, sys
from base64 import b64encode
from jinja2 import Template
import logging

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import getTemplate


# Notes:
# Use "powershell.exe -noexit" for testing


@DataTracker
def makePowershellDownloadAndExecuteBinary(url: str, path: str) -> AceStr:
    templateFile = 'download_exec_file.ps1'
    return AceStr('')


@DataTracker
def makePowershellDownloadAndExecuteMemPs1(url: str) -> AceStr:
    templateFile = 'download_exec_ps_enc_mem.ps1'
    template = getTemplate('make/powershell/', templateFile)
    script = template.render(
        url=url
    )
    return AceStr(script)


@DataTracker
def makePowershellMessageBox() -> AceStr: 
    templateFile = 'messagebox.ps1'
    template = getTemplate('make/powershell/', templateFile)
    script = template.render()
    return AceStr(script)


@DataTracker
def makePowershellCommand(input: str) -> AceStr:
    """For use with 'PowerShell.exe -Command {}'"""
    ret = toPowershellLine(input)
    return AceStr(ret)


@DataTracker
def makePowershellEncodedCommand(input: str) -> AceStr:
    """For use with 'PowerShell.exe -EncodedCommand {}'"""
    text = toPowershellLine(input)
    # https://stackoverflow.com/questions/71642299/how-to-use-python-to-represent-the-powershell-tobase64string-function
    text = bytearray(text, 'utf-16-le')
    b64 = b64encode(text).decode() # bytearray to str
    return AceStr(b64)


def toPowershellLine(input: AceStr) -> AceStr:
    """Tries converting file-content with powershell code into a single line"""
    # check if there's a ; at the end of each line
    lines = input.splitlines()
    for line in lines:
        line = line.strip()
        if not line.endswith(';'):
            logging.warn("Powershell script without ';' at end of line: {}".format(line))

    # remove all newlines
    input = input.replace('\r\n', '')
    input = input.replace('\n', '')

    return input
