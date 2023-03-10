# Recipe Overview

## PY#RATION 1.0

* ZIP -> LNK -> CMD -> BAT -> (WSCRIPT -> BAT, WSCRIPT -> BAT -> BAT -> (unrar.exe, EXE)
* Implement Version 1.0 of PY#RATION
* [https://www.securonix.com/blog/security-advisory-python-based-pyration-attack-campaign/](https://www.securonix.com/blog/security-advisory-python-based-pyration-attack-campaign/)
* Contains binaries without source
* Modifies filesystem or registry

![pyration10](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/pyration10.gif?raw=true)

```
python3 ace.py --recipe pyration10
```

Entry path: /pyration10/pyration10-documents.zip


## Ursnif

* ISO -> lnk -> bat -> wscript -> rundll32 -> download:cmd -> MSHTA -> reg:activex -> reg:powershell -> download:cmd -> download-bits:ps -> ps -> MessageBox
* Ursnif (Gozi, ISFB) incident from August 2022 analysis by thedfirreport
* [https://thedfirreport.com/2023/01/09/unwrapping-ursnifs-gifts/](https://thedfirreport.com/2023/01/09/unwrapping-ursnifs-gifts/)
* Contains binaries without source
* Modifies filesystem or registry

![ursnif](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/ursnif.gif?raw=true)

```
python3 ace.py --recipe ursnif
```

Entry path: None


## PY#RATION 1.6

* ZIP -> LNK -> CMD -> BAT -> (WSCRIPT -> BAT, WSCRIPT -> BAT -> BAT -> (unrar.exe, EXE)
* Implement Version 1.6 of PY#RATION
* [https://www.securonix.com/blog/security-advisory-python-based-pyration-attack-campaign/](https://www.securonix.com/blog/security-advisory-python-based-pyration-attack-campaign/)
* Contains binaries without source
* Modifies filesystem or registry

![pyration16](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/pyration16.gif?raw=true)

```
python3 ace.py --recipe pyration16
```

Entry path: /pyration16/pyration16-documents.zip


## Raspberry Robin

* LNK -> BAT -> MSIEXEC -> odbcconf:rundll32:dll
* [https://redcanary.com/blog/raspberry-robin/](https://redcanary.com/blog/raspberry-robin/)

![raspberryrobin](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/raspberryrobin.gif?raw=true)

```
python3 ace.py --recipe raspberryrobin
```

Entry path: /raspberryrobin.iso


## Recipe 3

* MSHTA -> Powershell:MessageBox
* Test Recipe 3

![recipe3](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/recipe3.gif?raw=true)

```
python3 ace.py --recipe recipe3
```

Entry path: /test.hta


## Emotet 1

* ZIP -> LNK -> Powershell.exe -> psScript:(Download:DLL, regsvr32.exe:DLL) <- c2:bat
* Emotet incident from June 2022 analysis by thedfirreport
* [https://thedfirreport.com/2022/11/28/emotet-strikes-again-lnk-file-leads-to-domain-wide-ransomware/](https://thedfirreport.com/2022/11/28/emotet-strikes-again-lnk-file-leads-to-domain-wide-ransomware/)
* Modifies filesystem or registry

![emotet1](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/emotet1.gif?raw=true)

```
python3 ace.py --recipe emotet1
```

Entry path: /emotet1/emotet1.zip


## Recipe 1

* HTML Smuggling -> ISO -> ( LNK -> Powershell:Load&Exec <- DLL )
* Test Recipe 1

![recipe1](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/recipe1.gif?raw=true)

```
python3 ace.py --recipe recipe1
```

Entry path: /test


## Recipe 4

* OneNote -> Bat -> ftp.exe -> PowerShell:MessageBox
* Test Recipe 4

![recipe4](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/recipe4.gif?raw=true)

```
python3 ace.py --recipe recipe4
```

Entry path: /test.one


## Recipe 2

* ZIP -> VBS -> Powershell:Download+Exec <- Powershell-Messagebox
* Test Recipe 2

![recipe2](https://github.com/dobin/ace-firefist/blob/main/docs/gifs/recipe2.gif?raw=true)

```
python3 ace.py --recipe recipe2
```

Entry path: /test.zip



