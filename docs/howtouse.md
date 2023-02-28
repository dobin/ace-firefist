# How To Use

This document explains how to create Makers and Recipes in ACE.


## Structure

The folder `make/` contains directories of python code which
create certain things, be it ZIP files, Onenote phishing file or
powershell loaders. These makers implement Techniques from TTP.

Structure:
* make/thing/thing.py: makeTheThing(stuff: AceBytes) -> AceStr
* make/thing/thing-template.txt
* make/thing/thing-template.txt.yaml


## Makers

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


## URL Routes

Serve any data (usually created by a maker) at a URL with `AceRoute()`. 
Use `serve()` to start a webserver serving them.

```py
thething: AceStr = ...
thingFile: AceRoute = makeAceRoute('/the.thing', thething)
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


## Make Better

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
INFO: --[ x: makeTheThing(y) -> x
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


## Make Templates

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
    template = getTemplate('make/thing/thing-template.txt)
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

