import logging
import requests as req

from model import *
import config


@PluginDecorator
def readFileContent(filename) -> AceBytes:
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
    aceFile = AceFile(name, data)
    if config.ENABLE_SCANNING is not None:
        scanAv(aceFile)
    return aceFile


def scanAv(aceFile: AceFile) -> bool:
    data = aceFile.data
    filename = aceFile.name
    params = { 'filename': filename }

    if config.ENABLE_SCANNING is False:
        return False

    url = config.ENABLE_SCANNING
    res = req.post(f"{url}/scan", params=params, data=data)
    jsonRes = res.json()

    if res.status_code != 200:
        print("Err: " + str(res.status_code))
        print("Err: " + str(res.text))
        return False
    
    ret_value = jsonRes['detected']

    logger.info("---[ Generating AceFile {}, detected: {}".format(filename, ret_value))
    return ret_value
