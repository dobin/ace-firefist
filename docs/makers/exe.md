Module exe
==========

Functions
---------

    
`makePeExecCmd(bat: str, asDll: bool) ‑> model.AceBytes`
:   Returns an exe/dll which will execute input as bat

    
`makePeExecCmdC2(baseUrl: str, url: str, asDll: bool) ‑> model.AceBytes`
:   Returns an exe/dll which will download & exec bat from baseUrl/url