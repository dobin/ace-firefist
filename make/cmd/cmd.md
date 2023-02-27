# cmd: command line

## Multiple commands in one line

From [stackoverflow](https://stackoverflow.com/questions/8055371/how-do-i-run-two-commands-in-one-line-in-windows-cmd):

You can use the special characters listed in the following table to pass multiple commands.

```
& [...]
command1 & command2
```

Use to separate multiple commands on one command line. Cmd.exe runs the first command, and then the second command.

```
&& [...]
command1 && command2
```
Use to run the command following && only if the command preceding the symbol is successful. Cmd.exe runs the first command, and then runs the second command only if the first command completed successfully.

```
|| [...]
command1 || command2
```
Use to run the command following || only if the command preceding || fails. Cmd.exe runs the first command, and then runs the second command only if the first command did not complete successfully (receives an error code greater than zero).

```
( ) [...]
(command1 & command2)
```
Use to group or nest multiple commands.

```
; or ,
command1 parameter1;parameter2
```
Use to separate command parameters.
