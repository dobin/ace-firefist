Module powershell
=================

Functions
---------

    
`makePsCommandFromPsScript(input: str) ‑> model.AceStr`
:   Make input compatible with 'PowerShell.exe -Command {}'

    
`makePsEncodedCommand(input: str) ‑> model.AceStr`
:   Make input compatible with "PowerShell.exe -EncodedCommand {}"

    
`makePsScriptMessagebox() ‑> model.AceStr`
:   Return a PsScript which simply outputs a popup

    
`makePsScriptToCmdByDownloadCmd(url: str) ‑> model.AceStr`
:   Return a PsScript which downloads and executes Cmdline with 'cmd /c'

    
`makePsScriptToPsCommandByDownloadCmd(url: str) ‑> model.AceStr`
:   Return a PsScript which downloads and executes a PsCommand with 'powershell -c'

    
`makePsScriptToPsCommandByDownloadIe(url: str) ‑> model.AceStr`
:   Return a PsScript which downloads and executes PsCommand with 'Invoke-Expression'

    
`toPowershellLine(input: model.AceStr) ‑> model.AceStr`
:   Tries converting file-content with powershell code into a single line