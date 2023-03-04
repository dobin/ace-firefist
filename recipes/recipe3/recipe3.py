from typing import List

from make.htmlsmuggling.htmlsmuggling import makeHtmlSmuggling
from make.lnk.lnk import makeLnk
from make.iso.iso import makeIso
from make.powershell.powershell import *
from make.zip.zip import makeZip
from make.vbs.vbs import *
from make.hta.hta import *
from make.onenote.onenote import *
from make.bat.bat import *
from make.cmd.cmd import *

from helpers import readFileContent, saveAceFile, makeAceFile
from model import *
from web import serve


def recipe3(baseUrl) -> List[AceRoute]:
    # MSHTA -> Powershell:MessageBox
    routes = []

    # PS: MessageBox
    psScript: AceStr = makePsScriptMessagebox()
    cmd: AceStr = makeCmdFromPsScript(psScript, encode=True, fullpath=False)

    # MSHTA
    hta: AceStr = makeHtaFromCmdByJscriptWscript(cmd)
    htaFile: AceFile = makeAceFile("test.hta", hta)  # not really needed
    containerServe: AceRoute = makeAceRoute('/test.hta', hta, download=True, downloadName='test.hta')
    routes.append(containerServe)
    return(routes)

