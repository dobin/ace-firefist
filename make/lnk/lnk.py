import argparse
import io
import os, sys

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import lib.pylnk3.helpers
from model import *


# Notes:
# - windows will not show more than 260 chars of the lnk argument - but they still exist


@DataTracker
def makeLnk(name: str, target: str, arguments: str, window_mode='Minimized', iconPath="", iconIndex=0) -> AceBytes:
    """Make a .lnk file with `name` pointing to `target` having `arguments` as arguments"""
    lnk = lib.pylnk3.helpers.for_file(
        target, 
        lnk_name=name, 
        arguments=arguments, 
        window_mode=window_mode,
        is_file=True,
        icon_file=iconPath,
        icon_index=int(iconIndex))
    lnkFileData = io.BytesIO()
    lnk.write(lnkFileData)
    return AceBytes(lnkFileData.getvalue())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='target path')
    parser.add_argument('--arguments', help='arguments')
    parser.add_argument('--name', help='lnk filename to create')
    args = parser.parse_args()

    lnkData = makeLnk(
        args.name,
        args.target,
        args.arguments,
    )

    # python3 -m make.lnk.lnk --name shortcut.lnk --target C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe --arguments "-noexit -command ls"    
    file = open(args.name, 'wb')
    file.write(lnkData)
    file.close()


if __name__ == "__main__":
    main()