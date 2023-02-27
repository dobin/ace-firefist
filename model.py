import logging
import config
from pathlib import Path
import inspect 

logger = logging.getLogger('basic_logger')



class RecipeInfo():
    def __init__(self, name, description, chain, reference, binaries, modify_filesystem, routes=[]):
        self.name = name
        self.description = description
        self.chain = chain
        self.routes = routes
        self.reference = reference
        self.binaries = binaries
        self.modify_filesystem = modify_filesystem


class AceStr(str):
    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj.index = GetCounter()
        return obj


class AceBytes(bytes):
    def __new__(cls, value):    
        obj = bytes.__new__(cls, value)
        obj.index = GetCounter()
        return obj
    


class AceFile():
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.data = data
        self.index = GetCounter()



def GetCounter():
    c = config.COUNTER
    config.COUNTER += 1
    return c


def prePrint(arg):
    s = []

    argType = str(type(arg))

    if 'AceBytes' in argType or 'AceStr' in argType or 'AceFile' in argType:
        s.append(str(arg.index))
    elif 'list' in argType:
        for item in arg:
            t = str(type(item))  # no inheritance, take type instead of isinstance()
            if 'AceBytes' in t or 'AceStr' in t:
                s.append(str(item.index))
    return ', '.join(s)


def DataTracker(func):
    def wrapper(*args, **kwargs):
        s = ''

        makerCounter = config.MAKER_COUNTER
        config.MAKER_COUNTER += 1

        # An Indent based on call stack would be useful
        indent = ""
        for n in (1, 3, 5, 7, 9, 11):  # skip wrappers
            parentName = inspect.stack()[n].function
            if parentName.startswith('make'):
                indent += "  "
            else:
                break
        for arg in args:
            s += prePrint(arg)
        for _, arg in kwargs.items():
            s += prePrint(arg)
        logger.info("--[ {}: {} {}({}) ".format(config.COUNTER, indent, func.__name__, s))
        config.makerCallstack[makerCounter] = "--[ {}: {} {}({})".format(config.COUNTER, indent, func.__name__, s)

        ret = func(*args, **kwargs)

        # What follows: Try to print ACE information of args+ret

        retType = str(type(ret))
        if 'AceBytes' in retType or 'AceStr' in retType or 'AceFile' in retType:
            index = ret.index
        else:
            index = GetCounter()

        logger.info("--[ {}: {} -> {}".format(config.COUNTER, indent, index))
        config.makerCallstack[makerCounter] += " -> {}".format(index)

        #elif isinstance(ret, list) and all(isinstance(e, AceFile) for e in ret):  # necessary?
        #    for file in ret:
        #        logger.info("--[ {}: {}({}) -> {}".format(config.COUNTER, func.__name__, s, file.index))

        # Dump content to files
        if not config.ENABLE_SAVING:
            return ret
        
        filename = None
        filedata = None

        if 'AceBytes' in retType:
            filename = "out/out_{}_{}.bin".format(index, func.__name__)
            filedata = ret
        elif 'AceStr' in retType:
            filename = "out/out_{}_{}.txt".format(index, func.__name__)
            filedata = bytes(ret, 'utf-8')
        
        elif 'bytes' in retType or 'bytesarray' in retType:
            filename = "out/out_{}_{}.bin".format(index, func.__name__)
            filedata = ret
        elif 'str' in retType:
            filename = "out/out_{}_{}.txt".format(index, func.__name__)
            filedata = bytes(ret, 'utf-8')
        
        elif 'AceFile' in retType:
            filename = "out/out_{}_file_{}".format(index, ret.name)
            filedata = ret.data
            if isinstance(filedata, str):
                filedata = bytes(filedata, 'utf-8')
        else:
            logger.warn("Wrong return type: {}".format(retType))
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
def enableTemplateInfo():
    config.SHOW_TEMPLATE_INFO = True
