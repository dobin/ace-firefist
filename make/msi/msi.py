import argparse
import io
import os, sys
import logging

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *

logger = logging.getLogger()

# install wix from https://github.com/wixtoolset/wix3
# candle.exe evil-rick.xml
# light.exe -out evil-rick.msi evil-rick.wixobj
# 


@DataTracker
def makeMsiFromCmd(input: AceStr) -> AceBytes:
    template = 'make/msi/evil-rick.msi' # https://0xrick.github.io/hack-the-box/ethereal/#Creating-Malicious-msi-and-getting-root
    placeholderLen = 512
    placeholder = b"A" * placeholderLen
    exchange = input + (" " * (placeholderLen - len(input)))
    exchangeBytes = bytes(exchange, 'ascii')
    if len(input) > placeholderLen:
        logger.error("  Input larger than {} bytes, template too small".format(placeholderLen))
    if len(placeholder) != len(exchangeBytes):
        logging.error("makeOnenoteBat: len not equal, something went wrong: {} {}".format(len(placeholder), len(exchangeBytes)))

    file = open(template, 'rb')
    data = file.read()
    file.close()

    print("Index of: {}".format(data.index(placeholder)))
    # replace the placeholder in our bat file
    data = data.replace(placeholder, exchangeBytes)
    return AceBytes(data)
