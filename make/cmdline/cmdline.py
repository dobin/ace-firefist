import os, sys
from base64 import b64encode
from jinja2 import Template
import logging
from typing import List

from model import *
from helpers import *

FTP_MAX_LINE_LENGTH = 230


@DataTracker
def makeCmdlineToCmdlineWithFtp(cmd: AceStr, file: str="%lOcAlApPdATA%\Temp\conf.log") -> AceStr:
    """Returns a cmdline which creates a file with a cmdline, which will be executed with 'ftps -s'"""
    if len(cmd) > FTP_MAX_LINE_LENGTH:
        raise Exception("makeBatFtpExec: command len {} is longer than FTP max of about {}, this will not work".format( 
            len(cmd), FTP_MAX_LINE_LENGTH))

    script = renderTemplate(
        'make/cmdline/ftp-exec.bat',
        command=cmd,
        file=file,
    )
    return AceStr(script)


@DataTracker
def makeCmdline(cmds: List[str]) -> AceStr:
    '''Returns a cmdline to cmd.exe with args "/c cmd[0] & cmd[0] & ..."'''
    s = "cmd /c"
    s += "&".join(cmds)
    return AceStr(s)
