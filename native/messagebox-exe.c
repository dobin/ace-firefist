#include <windows.h>
#include <stdio.h>


void makeMessageBox(void)
{
    printf("makeMessageBox()");
    MessageBox(NULL, "Hack the Gibson", "EvilDll", MB_OK);;
}


int main(int argc, char **argv) {
    makeMessageBox();
}