REM phase1
del %tmp%\front.bat
del %tmp%\b.bat
del %tmp%\c.bat
del %tmp%\settings.bat
del %tmp%\inv.vbs
del %tmp%\45b8f95j17.bat
del %tmp%\document.jpg


REM after moving to %localappdata%
del %localappdata%\Cortana\setup\assist.rar
del %localappdata%\Cortana\setup\unrar.cert
del %localappdata%\Cortana\setup\unrar.exe
del %localappdata%\Cortana\setup\setup.rar
rmdir %localappdata%\Cortana\setup\

del %localappdata%\Cortana\CortanaDefault.bat
del %localappdata%\Cortana\CortanaAssistance.exe
del %localappdata%\Cortana\inv.vbs
del %localappdata%\Cortana\ctask.exe
rmdir %localappdata%\Cortana
