import logging

from model import *


@PluginDecorator
def readFileContent(filename) -> bytes:
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return AceBytes(data)


def saveAceFile(file: AceFile):
    f = open(file.name, 'wb')
    f.write(file.data)
    f.close()
    logging.info("Written file: {}".format(file.name))


@PluginDecorator
def makeAceFile(name: str, data: bytes) -> AceFile:
    return AceFile(name, data)
