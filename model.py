import logging


COUNTER = None

def enableOut():
    global COUNTER
    COUNTER = 0


def PluginDecorator(func):
    def wrapper(*args, **kwargs):
        global COUNTER

        logging.info("--[ {}: {}".format(COUNTER, func.__name__))

        ret = func(*args, **kwargs)

        if COUNTER is None:
            return ret
        
        filename = None
        filedata = None

        if isinstance(ret, (bytes, bytearray)):
            filename = "out/out_{}_{}.bin".format(COUNTER, func.__name__)
            filedata = ret
        elif isinstance(ret, str):
            filename = "out/out_{}_{}.txt".format(COUNTER, func.__name__)
            filedata = bytes(ret, 'utf-8')
        elif isinstance(ret, AceFile):
            filename = "out/out_{}_file_{}".format(COUNTER, ret.name)
            filedata = ret.data

            if isinstance(filedata, str):
                filedata = bytes(filedata, 'utf-8')
        else:
            print("Wrong return type: {}".format(type(ret)))
            return ret
        
        f = open(filename, 'wb')
        f.write(filedata)
        f.close()

        COUNTER += 1
        
        return ret
    return wrapper


class AceRoute():
    def __init__(self, url: str, data: bytes, download: bool=False, downloadName=''):
        self.url = url
        self.data = data
        self.download = download
        self.downloadName = downloadName


class AceFile():
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.data = data
