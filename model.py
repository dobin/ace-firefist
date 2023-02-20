import logging
import config

logger = logging.getLogger('basic_logger')


class AceStr(str):
    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj.index = config.COUNTER
        return obj


class AceBytes(bytes):
    def __new__(cls, value):    
        obj = bytes.__new__(cls, value)
        obj.index = config.COUNTER
        return obj


def prePrint(arg):
    s = []
    if isinstance(arg, (AceBytes, AceStr)):
        s.append(str(arg.index))
    elif isinstance(arg, AceFile):
        s.append(str(arg.data.index))
    elif isinstance(arg, list):
        for file in arg:
            s.append(str(file.data.index))
    #else:
    #    s += ', '
    return ', '.join(s)


def PluginDecorator(func):
    def wrapper(*args, **kwargs):
        config.COUNTER += 1
                
        ret = func(*args, **kwargs)

        # What follows: Try to print ACE information of args+ret
        # This is SLOW
        s = ''
        for arg in args:
            s += prePrint(arg)
        for _, arg in kwargs.items():
            s += prePrint(arg)
        if isinstance(ret, (AceBytes, AceStr)):
            logger.info("--[ {}: {}({}) -> {}".format(config.COUNTER, func.__name__, s, ret.index))
        elif isinstance(ret, AceFile):
            logger.info("--[ {}: {}({}) -> {}".format(config.COUNTER, func.__name__, s, ret.data.index))
        elif isinstance(ret, list) and isinstance(ret, list[AceFile]):  # necessary?
            for file in ret:
                logger.info("--[ {}: {}({}) -> {}".format(config.COUNTER, func.__name__, s, file.data.index))
        else:
            logger.info("--[ {}: {}".format(config.COUNTER, func.__name__))

        # Dump content to files
        if not config.ENABLE_SAVING:
            return ret
        
        filename = None
        filedata = None

        if isinstance(ret, AceBytes):
            filename = "out/out_{}_{}.bin".format(config.COUNTER, func.__name__)
            filedata = ret
        elif isinstance(ret, AceStr):
            filename = "out/out_{}_{}.txt".format(config.COUNTER, func.__name__)
            filedata = bytes(ret, 'utf-8')
        elif isinstance(ret, (bytes, bytearray)):
            filename = "out/out_{}_{}.bin".format(config.COUNTER, func.__name__)
            filedata = ret
        elif isinstance(ret, str):
            filename = "out/out_{}_{}.txt".format(config.COUNTER, func.__name__)
            filedata = bytes(ret, 'utf-8')
        elif isinstance(ret, AceFile):
            filename = "out/out_{}_file_{}".format(config.COUNTER, ret.name)
            filedata = ret.data
            if isinstance(filedata, str):
                filedata = bytes(filedata, 'utf-8')
        else:
            print("Wrong return type: {}".format(type(ret)))
            return ret
        
        f = open(filename, 'wb')
        f.write(filedata)
        f.close()

        return ret
    return wrapper


class AceRoute():
    def __init__(self, url: str, data: bytes, download: bool=False, downloadName: str='', downloadMime: str=None):
        self.url = url
        self.data = data
        self.download = download
        self.downloadName = downloadName
        self.downloadMime = downloadMime


def enableOut():
    config.ENABLE_SAVING = True


def enableScanning(server):
    config.ENABLE_SCANNING = server


def setListenIp(ip):
    config.LISTEN_IP = ip
def setListenPort(port):
    config.LISTEN_PORT = port

class AceFile():
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.data = data
