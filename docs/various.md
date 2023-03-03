# Various Notes

## Print in Jscript

```js
<script language="JScript">
	function Exec()	{
		var r = new ActiveXObject("WScript.Shell");
		r.Run("calc.exe")
	}
	Exec()

    var myVariable = "Hello World";
    window.alert(myVariable);
</script>
```

## Print in VBScript

```js
<script language="VBScript">
    Set shell = CreateObject("WScript.Shell")
    Set env = shell.Environment("Process")
    env("myVariable") = "Hello World"
    MsgBox env("myVariable")
</script>
```