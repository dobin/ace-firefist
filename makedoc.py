#!/usr/bin/python3

import os
from glob import glob
from helpers import *
from io import StringIO


class StringBuilder:
    _file_str = None

    def __init__(self):
        self._file_str = StringIO()

    def Add(self, str):
        self._file_str.write(str)

    def AddNl(self, str):
        self.Add(str)
        self.Add('\n')

    def __str__(self):
        return self._file_str.getvalue()


def getYamlForRecipeFile(filename):
    dirName = filename[:-3]  # remove the '.py' extension
    yamlFilename = "recipes/{}/{}.yaml".format(dirName, filename)

    p = Path(yamlFilename)
    if not p.is_file():
        # dont care
        return None

    with open(yamlFilename) as f:
        yamlData = yaml.safe_load(f)
        yamlData['recipename'] = dirName

    return yamlData


def buildMd(yamls):
    sb = StringBuilder()

    sb.AddNl('# Recipe Overview')
    sb.AddNl('')

    for yaml in yamls:
        sb.AddNl("# {}".format(yaml['name']))
        sb.AddNl('')
        sb.AddNl("* {}".format(yaml['chain']))
        if yaml['description'] is not None:
            sb.AddNl("* {}".format(yaml['description']))
        if yaml['reference'] is not None:
            sb.AddNl("* [{}]({})".format(yaml['reference'], yaml['reference']))
        if yaml['binaries'] is not None:
            sb.AddNl("* Contains binaries without source")
        if yaml['modify_filesystem'] is not None:
            sb.AddNl("* Modifies filesystem or registry")
        sb.AddNl('')
        sb.AddNl('```')
        sb.AddNl("python3 ace.py --recipe {}".format(yaml['recipename']))
        sb.AddNl('```')
        sb.AddNl('')
        sb.AddNl("Entry path: {}".format(yaml['entryurl']))
        sb.AddNl('')
        sb.AddNl('')

    return str(sb)


def main():
    yamls = []
    files = []
    files = getRecipePyFiles()
    for file in files:
        yamlData = getYamlForRecipeFile(file)
        yamls.append(yamlData)
    
    md = buildMd(yamls)
    print(md)


if __name__ == "__main__":
    main()
