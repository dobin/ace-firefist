Module cmd
==========

Functions
---------

    
`makeCmdAddReg(keyName, valueName, value, type) ‑> model.AceStr`
:   

    
`makeCmdFileDownloadWithCurl(url: str, destinationFile: str = None) ‑> model.AceStr`
:   Return a cmd to curl downloading url into destinationFile

    
`makeCmdFromPsCommand(psCommand: str, encode: bool, fullpath: bool = True, obfuscate: bool = False) ‑> model.AceStr`
:   Returns a cmd to powershell.exe with args "-Command/-EncodedCommand psCommand"

    
`makeCmdFromPsScript(psScript: str, encode: bool, fullpath: bool = True, obfuscate: bool = False) ‑> model.AceStr`
:   Returns a cmd to powershell.exe with args "-Command/-EncodedCommand psScript"

    
`makeCmdToDllWithOdbc(dllPath: str) ‑> model.AceStr`
:   Returns a cmd to odbc.exe which loads DLL from dllPath (no args, use DLL_PROCESS_ATTACH)

    
`makeCmdToDllWithRundll(dllPath: str, args='') ‑> model.AceStr`
:   Returns a cmd to rundll32.exe which loads DLL from dllPath (with args)

    
`makeCmdline(cmds: List[str]) ‑> model.AceStr`
:   Returns a cmd to cmd.exe with args "/c cmd[0] & cmd[0] & ..."