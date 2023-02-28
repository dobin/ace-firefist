# ACE Fire Fist 

Attack Chain Emulator. Like pwntools, but for initial execution. Like AtomicRedTeam, but the components are freely combinable. 

It can generate artefacts to implement Techniques in recipes. 

Makers:
* makePowershell*
* makeBat
* makeIso
* makeZip
* makeLnk
* makeOnenote
* makeVbs
* makeHta

These can be freely combined to perform complex multi-stage attack chains. This can be used for PurpleTeaming, EDR Usecase verifications. PoC's and RedTeam attacks development.

Additionally, the following Threat Actor's are available: 
* PY#RATION 1.0
* PY#RATION 1.6
* Raspberry Robin

These can also be used to test your CSIRT / Forensic investigation process. 
These are based on real threat actors. 
All malicious code has been removed, all source code reviewed and tested.
All binaries are compiled, or the recipe will be marked with `binaries`.


## Further Documentation

If you want to write code by yourself, be it Recipes or Makers: 
* [How To Use](docs/howtouse.md)

For an overview and more details about the recipes, see:
* [Recipe Overview](doc/recipe-overview.md)


## Example recipe: MSTHA with powershell code

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
* The HTA file executes powershell code by invoking `powershell -encodedcommand ...`, which shows a message box


Generate the artefacts and start the web server:
```sh
$ rm out/*; python3 ace.py --recipe recipe_3
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

Go to `http://localhost:5000` for a overview page with all above information. Open http://localhost:5000/test.hta to start the attach chain.

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
