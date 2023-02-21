import argparse
import io
import os, sys
import logging

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *

logger = logging.getLogger()

@DataTracker
def makeOnenoteFromBat(input: AceStr) -> AceBytes:
    template = 'make/onenote/Test-bat-800.one'
    placeholderLen = 700  # even tho we stored 800 spaces, it only works with a bit less
    placeholder = b" " * placeholderLen
    exchange = input + " " * (placeholderLen - len(input))
    exchangeBytes = bytes(exchange, 'ascii')
    if len(placeholder) != len(exchangeBytes):
        logging.error("makeOnenoteBat: len not equal, something went wrong: {} {}".format(len(placeholder), len(exchangeBytes)))

    # open original onenote
    file = open(template, 'rb')
    data = file.read()
    file.close()

    # replace the placeholder in our bat file
    data = data.replace(placeholder, exchangeBytes)
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