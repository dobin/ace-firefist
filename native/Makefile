
all: testdll testexe execcmd-exe execcmd-dll execcmdc2-exe execcmdc2-dll


# Msgbox
testexe:
	x86_64-w64-mingw32-gcc -o ../payloads/evil.exe test-exe.c
testdll: 
	x86_64-w64-mingw32-gcc -shared -o ../payloads/evil.dll test-dll.c

# Exec
execcmd-exe:
	x86_64-w64-mingw32-gcc -o ../payloads/execcmd.exe execcmd-exe.c 
execcmd-dll:
	x86_64-w64-mingw32-gcc -shared -o ../payloads/execcmd.dll execcmd-dll.c 

# Download & Exec
execcmdc2-exe:
	x86_64-w64-mingw32-gcc execcmdc2-exe.c -o ../payloads/execc2cmd.exe -lwinhttp -municode
execcmdc2-dll:
	x86_64-w64-mingw32-gcc execcmdc2-dll.c -shared -o ../payloads/execc2cmd.dll -lwinhttp 
