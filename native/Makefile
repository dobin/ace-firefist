
all: testdll testexe


testdll: 
	x86_64-w64-mingw32-gcc -shared -o ../payloads/evil.dll test-dll.c


testexe:
	x86_64-w64-mingw32-gcc -o ../payloads/evil.exe test-exe.c
