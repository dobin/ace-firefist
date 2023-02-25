from typing import List
import logging
import requests as req
from jinja2 import Template
from pathlib import Path
import yaml
import os
from base64 import b64encode

from model import *
import config

logger = logging.getLogger('basic_logger')



def base64encode(input: AceBytes) -> AceStr:
    data = b64encode(input).decode()
    return AceStr(data)


def getRecipeInfo(file: str, routes: List[AceRoute]):
    p = Path(file)
    if not p.is_file():
        # dont care
        return None

    with open(file) as f:
        yamlData = yaml.safe_load(f)

    return RecipeInfo(
        name=yamlData['name'],
        description=yamlData['description'],
        chain=yamlData['chain'],
        reference=yamlData['reference'],
        binaries=yamlData['binaries'],
        modify_filesystem=yamlData['modify_filesystem'],
        routes=routes)
    


def yamlHelp(file):
    file = file + ".yaml"

    p = Path(file)
    if not p.is_file():
        return

    with open(file) as f:
        yamlData = yaml.safe_load(f)

    #if not 'invalid' in yamlData:
    #    return
    #if not isinstance(yamlData['invalid'], list):
    #    return
    #exceptions = yamlData['invalid']
    #for exception in exceptions: 
    #print("Exceptions: " + str(exceptions))

    logger.info("--( Template {}:".format(file))
    entries = [ 'title', 'description', 'howtouse', 'input', 'invalid' ]
    for key in entries:
        if key in yamlData:
            logger.info("    {}: {}".format(key, yamlData[key]))


def getTemplate(directory: str, name: str) -> Template:
    path = os.path.join(directory, name)

    with open(path) as f:
        template = Template(f.read())

    if config.SHOW_TEMPLATE_INFO:
        yamlHelp(path)

    return template


@DataTracker
def renderTemplate(directory: str, name: str, **kwargs):
    template = getTemplate(directory, name)
    rendered = template.render(kwargs)
    return AceStr(rendered)


@DataTracker
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


@DataTracker
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
