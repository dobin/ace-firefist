REM lnk
del %tmp%\45b8f95j17.txt
del %tmp%\45b8f95j17.bat

REM phase1
del %tmp%\inv.vbs
del %tmp%\document.jpg
del %tmp%\settings.bat
del %tmp%\c.bat
del %tmp%\b.bat

REM after moving to %localappdata%
del %localappdata%\Cortana\setup\assist.rar
del %localappdata%\Cortana\setup\unrar.txt
del %localappdata%\Cortana\setup\unrar.exe
rmdir %localappdata%\Cortana\setup\

del %localappdata%\Cortana\CortanaDefault.bat
del %localappdata%\Cortana\CortanaAssistance.exe
del %localappdata%\Cortana\inv.vbs
rmdir %localappdata%\Cortana

