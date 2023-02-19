# ACE Fire Fist 

Attack Chain Emulator. Like pwntools, but for initial execution. 


## Example (recipe 3)

Generate a HTA file based on a template which executes powershell code (displaying a messge box),
and make it available via HTTP at `http://localhost:5001/test.hta`. 

Source:
```py
# MSHTA -> Powershell:MessageBox
def recipe_3():
    ps1msgbox = makePowershellMessageBox()
    ps1msgbox = makePowershellEncodedCommand(ps1msgbox)

    cmd = AceStr("powershell.exe -EncodedCommand {}".format(ps1msgbox))
    mshta = makeMshtaJscriptExec(cmd)
    mshtaFile: AceFile = makeAceFile("test.hta", mshta)

    containerServe: AceRoute = AceRoute('/test.hta', mshta, download=True, downloadName='test.hta')
    serve(containerServe)
```

Generate the artefacts and start the web server:
```sh
$ rm out/*; python3 ace.py --recipe 3
INFO: --[ 1: makePowershellMessageBox() -> 1
INFO: --[ 2: makePowershellEncodedCommand(1) -> 2
INFO: --[ 3: makeMshtaJscriptExec(2) -> 3
INFO: ---[ Generating AceFile test.hta, detected: False
INFO: --[ 4: makeAceFile(3) -> 3

Routes:
  /                       Recipe overview
  /out/<filename>         out/ files
  /static/<filename>      static/ files
  /test.hta          (3)  Download: True test.hta

 * Serving Flask app 'web' (lazy loading)
```

Go to `http://localhost:5001` for a overview page with all above information.

Generated files:
```
$ ls -1 out/
out_1_makePowershellMessageBox.txt
out_2_makePowershellEncodedCommand.txt
out_3_makeMshtaJscriptExec.txt
out_4_file_test.hta
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

