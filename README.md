# ACE Fire Fist 

Attack Chain Emulator. Like pwntools, but for initial access and executino. Like AtomicRedTeam, but the components can be freely combined. 

It can generate artefacts to implement techniques in recipes. 
Recipes use Makers, which can be freely combined to perform complex multi-stage attack chains.

Makers:
* makePowershell*
* makeBat
* makeIso
* makeZip
* makeLnk
* makeOnenote
* makeVbs
* makeHta

Additionally, the following threat actors recipes are available: 
* PY#RATION 1.0
* PY#RATION 1.6
* Raspberry Robin
* Ursnif

This can be used for PurpleTeaming, EDR Usecase verifications. PoC's and RedTeam attacks development.
These can also be used to test your CSIRT or forensic investigation process (CSIRT). 
Recipes are based on real attacks of known threat actors. 

All malicious code has been removed, all source code reviewed and tested.
All binaries can be recompiled (or the recipe will be marked with `binaries`).

Usage notes: 
* Disable AV if you want to execute the whole chain (only active EDR)
* Use it in a VM
* Most Threat Actor payloads dont have proxy support. A direct connection is prefered
* Use `cleanup.bat` to remove all artefacts on disk
* Recipes are tagged `binaries = [Files]` if they have binaries without source available (e.g. copied rundll32.exe)


## Further Documentation

If you want to write code by yourself, be it Recipes or Makers: 
* [How To Use](docs/howtouse.md) ACE for development

Makers overview: 
* [Makers](docs/makers/) list and API

For an overview and more details about the recipes, see:
* [Recipe Overview](docs/recipes.md)


## Example 

A recipe with uses MSTHA to execute powershell code.

This recipe 
generates a HTA file based on a template which executes powershell code (displaying a messge box),
and make it available via HTTP at http://localhost:5000/test.hta. Available as recipe 3. 

Source:
```py
# MSHTA -> Powershell:MessageBox
def recipe_3():
    ps1msgbox: AceStr = makePowershellMessageBox()
    ps1msgbox: AceStr = makePowershellEncodedCommand(ps1msgbox)

    cmd: AceStr = AceStr("powershell.exe -EncodedCommand {}".format(ps1msgbox))
    hta: AceStr = makeMshtaJscriptExec(cmd)
    htaFile: AceFile = makeAceFile("test.hta", hta)

    containerServe: AceRoute = makeAceRoute('/test.hta', hta, download=True, downloadName='test.hta')
    serve(containerServe)
```

While the packing flows forward, to see what the victim
is executing, look at it from bottom upwards:
* Access a URL `/test.hta` with the `test.hta` file and download it
* Execute the `test.hta` file by double clicking it
* The HTA file executes powershell code by invoking `powershell -encodedCommand ...`, which shows a message box


Generate the artefacts and start the web server:
```sh
$ rm out/*; python3 ace.py --recipe recipe_3
--[ 00:  makePsScriptMessagebox() -> 1
--[ 00:    renderTemplate(messagebox.ps1) -> 0
--[ 02:  makeCmdFromPsScript(1) -> 4
--[ 02:    makePsCommandFromPsScript(1) -> 2
--[ 03:    makeCmdFromPsCommand(2) -> 4
--[ 03:      makePsEncodedCommand(2) -> 3
--[ 05:  makeHtaFromCmdByJscriptWscript(4) -> 6
--[ 05:    renderTemplate(hta-jscript-exec.hta) -> 5
--[ 07:  makeAceFile(6) -> 7
--[ 08:  makeAceRoute(/test.hta, 6)

Routes:
  /                       Recipe overview
  /out/<filename>         out/ files
  /static/<filename>      static/ files
  /test.hta          (3)  Download: True test.hta

 * Serving Flask app 'web' (lazy loading)
```

Go to `http://localhost:5000` for a overview page with all above information. Open http://localhost:5000/test.hta to start the attach chain.

Generated files:
```
$ ls -1 out/
out_00_renderTemplate.txt
out_01_makePsScriptMessagebox.txt
out_02_makePsCommandFromPsScript.txt
out_03_makePsEncodedCommand.txt
out_04_makeCmdFromPsCommand.txt
out_04_makeCmdFromPsScript.txt
out_05_renderTemplate.txt
out_06_makeHtaFromCmdByJscriptWscript.txt
out_07_file_test.hta
```

Video: 
```
<tbd>
```


## Install

```
$ pip install -r requirements.txt
$ sudo apt install rar
```

If you dont trust my binaries in `payloads/`:
```
$ sudo apt install mingw-w64
$ cd native
$ make
```


## Standalone example

See `example.py` for a standalone script recipe. 

Get inspiration from recipes from folder `recipes/`


## Directories

* `out/`: generated artefacts
* `static/`: files served in web server under `static/`
* `payload/`: files used as payloads (not served via web)


## Makers

The folder `make/` contains directories of python code which
create certain things, be it ZIP files, Onenote phishing file or
powershell loaders. These makers implement Techniques from TTP.
See [How To Use](docs/howtouse.md) on how to develop them.

Structure:
* make/thing/thing.py: makeTheThing(stuff: AceBytes) -> AceStr
* make/thing/thing-template.txt
* make/thing/thing-template.txt.yaml


## Libraries

* libs/pylnk3: pylnk3-dev, as it has an important bugfix. No deps. GPL3.
* libs/librar: librar, with patched for python3 and some smaller things. No deps. No License.


## Generate Docs

For makers: [pdoc3](https://pdoc3.github.io/pdoc/)
```
$ cd ace-firefist/
$ bash makedoc.sh
```

For recipes: 


## Other related projects

* Atomic Redteaming: 
* Caldery: 
* Scyth: 
