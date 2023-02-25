#include <windows.h>

// From: https://blog.didierstevens.com/2017/09/08/quickpost-dlldemo/
// Compile: x86_64-w64-mingw32-gcc -shared -o test-dll.dll test-dll.c
// Run: rundll32.exe test-dll.dll,makeMessageBox


extern __declspec(dllexport) void makeMessageBox(void)
{
    OutputDebugString("ExportedFunction: makeMessageBox");
    MessageBox(NULL, "Hack the Gibson", "EvilDll", MB_OK);;
}
 

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        OutputDebugString("DLL_PROCESS_ATTACH");
        break;
 
    case DLL_THREAD_ATTACH:
        OutputDebugString("DLL_THREAD_ATTACH");
        break;
 
    case DLL_THREAD_DETACH:
        OutputDebugString("DLL_THREAD_DETACH");
        break;
 
    case DLL_PROCESS_DETACH:
        OutputDebugString("DLL_PROCESS_DETACH");
        break;
    }
 
    return TRUE;
}