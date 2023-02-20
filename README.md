# ACE Fire Fist 

Attack Chain Emulator. Like pwntools, but for initial execution. 

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


## Example recipe: MSTHA with powershell code

Generate a HTA file based on a template which executes powershell code (displaying a messge box),
and make it available via HTTP at http://localhost:5000/test.hta. Available as recipe 3. 

Source:
```py
# MSHTA -> Powershell:MessageBox
def recipe_3():
    ps1msgbox: AceStr = makePowershellMessageBox()
    ps1msgbox: AceStr = makePowershellEncodedCommand(ps1msgbox)

    cmd: AceStr = AceStr("powershell.exe -EncodedCommand {}".format(ps1msgbox))
    mshta: AceStr = makeMshtaJscriptExec(cmd)
    mshtaFile: AceFile = makeAceFile("test.hta", mshta)

    containerServe: AceRoute = AceRoute('/test.hta', mshta, download=True, downloadName='test.hta')
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

## Directories

* `out/`: generated artefacts
* `static/`: files served in web server under `static/`
* `payload/`: files used as payloads (not served via web)


## Standalone example

See `example.py` for a standalone script recipe. 

Get inspiration from recipes from folder `recipes/`


## Recipes

### Recipe 1

HTML Smuggling -> ISO -> ( LNK -> Powershell:Load&Exec <- DLL )

```
python3 ace.py --recipe recipe_1
```

Entry URL: http://localhost:5000/test


### Recipe 2

ZIP -> VBS -> Powershell:Download+Exec <- Powershell-Messagebox

```
python3 ace.py --recipe recipe_2
```

Entry URL: http://localhost:5000/test.zip


### Recipe 3

MSHTA -> Powershell:MessageBox

```
python3 ace.py --recipe recipe_3
```

Entry URL: http://localhost:5000/test.hta


### Recipe 4

OneNote -> Bat -> Powershell:Messagebox

```
python3 ace.py --recipe recipe_4
```

Entry URL: http://localhost:5000/test.one


## Make

Structure:
* make/thing/thing.py: makeTheThing(stuff: AceBytes) -> AceStr
* make/thing/thing-template.txt
* make/thing/thing-template.txt.yaml


### Makers

The folder `make/` contains directories of python code which
create certain things, be it ZIP files, Onenote phishing file or
powershell loaders. These makers implement Techniques from TTP.

The makers usually take some kind of input, and generate and return a output with it. 
For example a c2 url for generating powershell loader code, or files to store in an iso. 

Examples:
* makePowershell*
* makeBat
* makeIso
* makeZip
* makeLnk
* makeOnenote
* makeVbs
* makeHta

How to extend ace: Simply create a normal python function in the file `make/<thing>/<thing>.py`. This is the interface to your thing. 
It should return `str` or `bytes`. Can take any parameters.

for example: `make/thing/thing.py`:
```py
def makeTheThing(stuff: str) -> bytes:
  return b"The stuff: " + stuff
```

Create a recipe like the `example.py` recipe, 
and combine it there with the other makers. 
More examples are in `recipes/`.

### Routes

Serve any data at a URL with `AceRoute()`. 
Use `serve()` to start a webserver serving them.

```py
thething: AceStr = ...
thingFile: AceRoute = AceRoute('/thething', thething)
serve([ thingFile ])
```

AceRoute:
```py
class AceRoute():
    def __init__(self, url: str, data: bytes, download: bool=False, downloadName: str='', downloadMime: str=None):
        self.url = url
        self.data = data
        self.download = download
        self.downloadName = downloadName
        self.downloadMime = downloadMime
```


### Make Better

Ace can track your data. It observes the data structures
`AceStr`, `AceBytes` and `AceFile` into makers decorated
with `DataTracker`. For example which powershell script
you insert into which executor, which files in a zip etc. 
These are indexed by numbers.

Example: 
```
INFO: --[ 1: makePowershellMessageBox() -> 1
INFO: --[ 2: makePowershellEncodedCommand(1) -> 2
INFO: --[ 3: makeMshtaJscriptExec(2) -> 3
INFO: --[ 4: makeAceFile(3) -> 3
```

To gain advantages of data tracking, use Ace data structures, and 
decorate your maker with `@DataTracker`:

```py
@DataTracker
def makeTheThing(stuff: AceStr) -> AceBytes:
  return AceBytes("The stuff: " + stuff)
```

Result:
```
INFO: --[ x: makeTheThing(x) -> y
```

Ace data structures: 
* str -> AceStr
* bytes -> AceBytes

And also:
```py
class AceFile():
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.data = data
```

### Templates

Use templates whenever possible when using text files.
The templates are one of the main assets of an ace. Each
is used to generate a specific thing together with its maker (`makeThing()`)
Prepare a file where
jinja2 can replace with placeholder `{{}}`.

Example: `make/thing/thing-template.txt`
```
The stuff: {{stuff}}
```

And use it in its corresponding function. 

Example: `make/thing/thing.py`:

```py
@DataTracker
def makeTheThing(stuff: AceStr) -> AceBytes:
    templateFile = 'thing-template.txt'
    template = getTemplate('make/thing/', templateFile)
    rendered = template.render(
        stuff=stuff,
    )
    return AceBytes(rendered)
```

Optionally: Store information about the template in the 
`<template>.yaml` file. It is not just for documentation
of your template, but will also be used by `getTemplate()`.

Example: `make/thing/thing-template.txt.yaml`
```
---
  title: "Create a thing file"
  author: "Me"
  date: 20220220
  description: "Creates things of type foo As seen in APT123"
  howtouse: "Input is a x86 exe"
  input: "A exe binary"
  restrictions: "only works for 32 bit"
  invalid: [ "\x00" ]
```

Show with `--templateinfo`


## Notes

```
rm out/*; ./ace.py ...
```


## Libraries

* libs/pylnk3: pylnk3-dev, as it has an important bugfix. No deps. GPL3

