import os, sys
from base64 import b64encode
from jinja2 import Template
import logging
from typing import List

from model import *
from helpers import *
from make.powershell.powershell import *


@DataTracker
def makeCmdAddReg(keyName: str, valueName: str, value: AceStr, type: str) -> AceStr:
    """Returns a cmd which will add a registry key"""
    s = "reg add \"{}\" /v \"{}\" /t {} /f /d \"{}\"".format(keyName, valueName, type, value)
    return AceStr(s)


@DataTracker
def makeCmdToDllWithOdbc(dllPath: str) -> AceStr:
    '''Returns a cmd to odbc.exe which loads DLL from dllPath (no args, use DLL_PROCESS_ATTACH)'''
    script = renderTemplate(
        'make/cmd/odbcconf-loaddll.cmd',
        dllPath=dllPath
    )
    return AceStr(script)


@DataTracker
def makeCmdToDllWithRundll(dllPath: str, args='') -> AceStr:
    '''Returns a cmd to rundll32.exe which loads DLL from dllPath (with args)'''
    script = renderTemplate(
        'make/cmd/rundll32-dll.cmd',
        dllPath=dllPath,
        args=args
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
