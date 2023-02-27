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
from model import AceFile, AceRoute
from web import serve


def recipe4(baseUrl) -> List[AceRoute]:
    # OneNote -> Bat -> ftp.exe -> PowerShell:MessageBox
    routes = []

    # PS: MessageBox
    psScript: AceStr = makePsScriptMessagebox()
    cmd: AceStr = makeCmdFromPsScript(psScript, encode=True, fullpath=False)
    bat = makeBatFromCmds([cmd])
    # batFile: AceFile = makeAceFile("test.bat", bat)  # for debugging

    # OneNote
    onenote = makeOnenoteFromBat(bat)
    #onenoteFile: AceFile = makeAceFile("test.one", onenote)  # for debugging

    # Serve
    containerServe: AceRoute = AceRoute('/test.one', onenote, download=True, downloadName='test.one')
    routes.append(containerServe)
    return(routes)


