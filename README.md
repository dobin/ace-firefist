# ACE Fire Fist 

Attack Chain Emulator. Like pwntools, but for initial execution. 


## Example (recipe 3)

Source:
```py
# MSHTA -> Powershell:MessageBox
def recipe_3():
    ps1msgbox = makePowershellMessageBox()
    ps1msgbox = makePowershellEncodedCommand(ps1msgbox)

    cmd = AceStr("powershell.exe -EncodedCommand {}".format(ps1msgbox))
    mshta = makeMshtaJscriptExec(cmd)

    containerServe: AceRoute = AceRoute('/test.hta', mshta, download=True, downloadName='test.hta')
    serve(containerServe)
```

Execute:
```sh
$ rm out/*; python3 ace.py --recipe 3
INFO:basic_logger:--[ 1: makePowershellMessageBox() -> 1
INFO:basic_logger:--[ 2: makePowershellEncodedCommand(1) -> 2
INFO:basic_logger:--[ 3: makeMshtaJscriptExec(2) -> 3

Routes:
  /                      Recipe overview
  /out/<filename>        out/ files
  /static/<filename>     static/ files
  /test.hta              (3)    Download: True test.hta

 * Serving Flask app 'web' (lazy loading)
```

Files:
```
$ ls -1 out/
out_1_makePowershellMessageBox.txt
out_2_makePowershellEncodedCommand.txt
out_3_makeMshtaJscriptExec.txt
```

Video: 
```
<tbd>
```

## Directories

* `out/`: generated artefacts
* `static/`: files served in web server under `static/`
* `payload/`: files used as payloads (not served via web)


## Recipes

### Recipe 1

HTML Smuggling -> ISO -> ( LNK -> Powershell:Load&Exec <- DLL )

```
python3 ace.py --recipe 1
```

Entry URL: http://localhost:5000/test


### Recipe 2

ZIP -> VBS -> Powershell:Download+Exec <- Powershell-Messagebox

```
python3 ace.py --recipe 2
```

Entry URL: http://localhost:5000/test.zip


### Recipe 3

MSHTA -> Powershell:MessageBox

```
python3 ace.py --recipe 3
```

Entry URL: http://localhost:5000/test.hta


## Notes

```
rm out/*; ./ace.py ...
```


## Libraries

* libs/pylnk3: pylnk3-dev, as it has an important bugfix. No deps. 

