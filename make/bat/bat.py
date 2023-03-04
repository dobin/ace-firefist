import os, sys
from base64 import b64encode
from jinja2 import Template
import logging
from typing import List

from model import *
from helpers import getTemplate

FTP_MAX_LINE_LENGTH = 230


@DataTracker
def makeBatFromCmdByFtp(command: AceStr, file: str="%lOcAlApPdATA%\Temp\conf.log") -> AceStr:
    if len(command) > FTP_MAX_LINE_LENGTH:
        logging.warn("makeBatFtpExec: command len {} is longer than FTP max of about {}, this will not work".format( 
            len(command), FTP_MAX_LINE_LENGTH))

    template = getTemplate('make/bat/ftp-exec.bat')
    script = template.render(
        command=command,
        file=file,
    )
    return AceStr(script)


@DataTracker
def makeBatFromCmds(cmds: List[str]) -> AceStr:
    return AceStr('\r\n'.join(cmds))
