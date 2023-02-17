
COUNTER = 0

def disableOut():
    COUNTER = None


def PluginDecorator(func):
    def wrapper(*args, **kwargs):
        global COUNTER

        ret = func(*args, **kwargs)

        if COUNTER is None:
            return ret
        
        filename = None
        filedata = None

        if isinstance(ret, (bytes, bytearray)):
            filename = "out/out_{}.bin".format(COUNTER)
            filedata = ret
        elif isinstance(ret, AceFile):
            filename = "out/out_{}.{}".format(COUNTER, ret.name)
            filedata = ret.data
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
    def __init__(self, url: str, data: bytes):
        self.url = url
        self.data = data


class AceFile():
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.data = data
