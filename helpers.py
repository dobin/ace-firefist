from model import AceFile, PluginDecorator


@PluginDecorator
def readFileContent(filename) -> bytes:
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data


def saveAceFile(file: AceFile):
    f = open(file.name, 'wb')
    f.write(file.data)
    f.close()


@PluginDecorator
def makeAceFile(name: str, data: bytes) -> AceFile:
    return AceFile(name, data)
