Module cmdline
==============

Functions
---------

    
`makeCmdline(cmds: List[str]) ‑> model.AceStr`
:   Returns a cmdline to cmd.exe with args "/c cmd[0] & cmd[0] & ..."

    
`makeCmdlineToCmdlineWithFtp(cmd: model.AceStr, file: str = '%lOcAlApPdATA%\\Temp\\conf.log') ‑> model.AceStr`
:   Returns a cmdline which creates a file with a cmdline, which will be executed with 'ftps -s'