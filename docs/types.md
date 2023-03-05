# Types

## cmd

*cmd*:
* `[path to exe] [args]`
* example: `net.exe user administrator`
* `cmd.exe [path] [args]`
* only one executable with its args

*cmdline*: 
* cmd line, like input line in cmd.exe shell
* can execute multiple commands with `&`
* example: `net.exe user administrator & hostname`
* `cmd.exe /c <cmdline>`

*batfile*
* a file.bat
* multiple lines
* `cmd.exe [batfile]` or `.\file.bat`

cmd uses `^` as escape character. Quotes can be doubled: `""` = `"` (in most circumstances)

## powershell

*psCommand*: 
* powershell line, like input line in powershell.exe shell
* multiple psCommands with `;`
* example: `[System.Windows.MessageBox]::Show($msgBody); ls`
* `powershell.exe -Command [psCommand]`

*psEncodedCommand*:
* psCommand base64 encoded
* `powershell.exe -EncodedCommand [psEncodedCommand]`

psScript
* a file.ps1
* multiple lines
* `powershell.exe file.ps1`

Powershell uses ` as escape character. It can be doubled too.