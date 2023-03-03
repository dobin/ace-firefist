import argparse
import io
import os, sys
import logging

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import *

logger = logging.getLogger()


@DataTracker
def makeOnenoteFromBat(input: AceStr) -> AceBytes:
    template = 'make/onenote/Test-bat-800.one'
    placeholderLen = 700  # even tho we stored 800 spaces, it only works with a bit less 

    if len(input) > placeholderLen:
        raise Exception("  Input larger than {} bytes, template too small".format(placeholderLen))

    placeholder = b" " * placeholderLen
    exchange = input + " " * (placeholderLen - len(input))
    exchangeBytes = bytes(exchange, 'ascii')
 
    file = open(template, 'rb')
    data = file.read()
    file.close()

    data = replacer(data, placeholder, exchangeBytes)

    return AceBytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='')
    parser.add_argument('--data', help='')
    args = parser.parse_args()

    lnkData = makeOnenoteFromBat(
        args.data,
    )

    file = open(args.name, 'wb')
    file.write(lnkData)
    file.close()


if __name__ == "__main__":
    main()