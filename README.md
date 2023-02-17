# ACE Fire Fist 

Attack Chain Emulator. Like pwntools, but for initial execution. 


```
rm out/*; ./ace.py ...
```

# Recipes

## recipe 1: 

HTML Smuggling -> ISO -> ( LNK -> Powershell:Load&Exec <- DLL )

```
python3 ace.py --recipe 1
```

URL: http://localhost:5000/test


## recipe 2

ZIP -> VBS -> Powershell:Download+Exec <- Powershell-Messagebox

```
python3 ace.py --recipe 2
```

URL: http://localhost:5000/test.zip


## recipe 3

MSHTA -> Powershell:MessageBox

```
python3 ace.py --recipe 3
```

URL: http://localhost:5000/test.hta


# Example 

All artefacts get logged in `out/`:
```
out_0_file_evil.dll
out_1_makePowershell.txt
out_2_makeLnk.bin
out_3_file_clickme.lnk
out_4_makeIso.bin
out_5_file_test2.iso
out_6_makeHtmlSmuggling.txt
```


# Libraries

* libs/pylnk3: pylnk3-dev, as it has an important bugfix. No deps. 

