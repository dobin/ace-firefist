# Recipe Overview

## PY#RATION 1.0

* Implement Version 1.0 of PY#RATION
* [https://www.securonix.com/blog/security-advisory-python-based-pyration-attack-campaign/](https://www.securonix.com/blog/security-advisory-python-based-pyration-attack-campaign/)
* Contains binaries without source
* Modifies filesystem or registry

```
python3 ace.py --recipe pyration10
```

Entry path: /pyration10/pyration10-documents.zip


## Raspberry Robin

* ISO -> lnk -> bat -> wscript -> rundll32 -> download:cmd -> MSHTA -> reg:activex -> reg:powershell -> download:cmd -> download-bits:ps -> ps -> MessageBox
* Ursnif (Gozi, ISFB) incident from August 2022 analysis by thedfirreport
* [https://thedfirreport.com/2023/01/09/unwrapping-ursnifs-gifts/](https://thedfirreport.com/2023/01/09/unwrapping-ursnifs-gifts/)
* Contains binaries without source
* Modifies filesystem or registry

```
python3 ace.py --recipe ursnif
```

Entry path: None


## PY#RATION 1.6

* Implement Version 1.6 of PY#RATION
* [https://www.securonix.com/blog/security-advisory-python-based-pyration-attack-campaign/](https://www.securonix.com/blog/security-advisory-python-based-pyration-attack-campaign/)
* Contains binaries without source
* Modifies filesystem or registry

```
python3 ace.py --recipe pyration16
```

Entry path: /pyration16/pyration16-documents.zip


## Raspberry Robin

* LNK -> BAT -> MSIEXEC -> odbcconf:rundll32:dll
* [https://redcanary.com/blog/raspberry-robin/](https://redcanary.com/blog/raspberry-robin/)

```
python3 ace.py --recipe raspberryrobin
```

Entry path: /raspberryrobin.iso


## Recipe 3

* MSHTA -> Powershell:MessageBox
* Test Recipe 3

```
python3 ace.py --recipe recipe3
```

Entry path: /test.hta


## Recipe 1

* HTML Smuggling -> ISO -> ( LNK -> Powershell:Load&Exec <- DLL )
* Test Recipe 1

```
python3 ace.py --recipe recipe1
```

Entry path: /test


## Recipe 4

* OneNote -> Bat -> ftp.exe -> PowerShell:MessageBox
* Test Recipe 4

```
python3 ace.py --recipe recipe4
```

Entry path: /test.one


## Recipe 2

* ZIP -> VBS -> Powershell:Download+Exec <- Powershell-Messagebox
* Test Recipe 2

```
python3 ace.py --recipe recipe2
```

Entry path: /test.zip



