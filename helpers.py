from model import AceFile

def readFileContent(filename):
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data


def saveAceFile(file: AceFile):
    f = open(file.name, 'wb')
    f.write(file.data)
    f.close()
    