# Recipe Overview

## Threat Actors

* PY#RATION 1.0
* PY#RATION 1.6
* Raspberry Robin


## Examples and Tests

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
