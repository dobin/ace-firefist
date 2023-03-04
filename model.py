import logging
import config
from pathlib import Path
import inspect 
from typing import List
import os
from functools import lru_cache, reduce, partial, wraps

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



def dumpDataToFile(index, funcName, ret, retType):
    filename = None
    filedata = None

    if 'AceBytes' in retType:
        filename = "out/out_{:02d}_{}.bin".format(index, funcName)
        filedata = ret
    elif 'AceStr' in retType:
        filename = "out/out_{:02d}_{}.txt".format(index, funcName)
        filedata = bytes(ret, 'utf-8')
    
    elif 'bytes' in retType or 'bytesarray' in retType:
        filename = "out/out_{:02d}_{}.bin".format(index, funcName)
        filedata = ret
    elif 'str' in retType:
        filename = "out/out_{:02d}_{}.txt".format(index, funcName)
        filedata = bytes(ret, 'utf-8')
    
    elif 'AceFile' in retType:
        filename = "out/out_{:02d}_file_{}".format(index, ret.name)
        filedata = ret.data
        if isinstance(filedata, str):
            filedata = bytes(filedata, 'utf-8')
    else:
        logger.warn("Wrong return type: {}".format(retType))
        return ret
    
    f = open(filename, 'wb')
    f.write(filedata)
    f.close()


def parseFuncAceArgs(arg) -> List[str]:
    s = [] # array of arguments
    argType = str(type(arg))

    # Stuff which has .index
    if 'AceBytes' in argType or 'AceStr' in argType or 'AceFile' in argType:
        s.append(str(arg.index))
    # lists of data which may have .index
    elif 'list' in argType:
        for item in arg:
            t = str(type(item))
            if 'AceBytes' in t or 'AceStr' in t or 'AceFile' in t:
                s.append(str(item.index))
    return s


def DataTracker(func):
    """Decorator to log Ace data structures on annotated functions"""

    @wraps(func)  # for pdoc3
    def wrapper(*args, **kwargs):
        makerCounter = config.MAKER_COUNTER
        config.MAKER_COUNTER += 1

        # An Indent based on call stack would be useful
        # Check if parents are already a make(er)
        indent = ""
        for n in (1, 3, 5, 7, 9, 11):  # skip wrappers
            parentName = inspect.stack()[n].function
            if parentName.startswith('make'):
                indent += "  "
            else:
                break

        allArgs = []
        s = ''        
        # check function name special cases
        funcName = str(func)
        if 'readFileContent' in funcName or 'renderTemplate' in funcName:
            allArgs.append(os.path.basename(str(args[0])))
        elif 'makeAceRoute' in funcName:
            allArgs.append(str(args[0]))
        
        # get arguments of the function
        for arg in args:
            allArgs += parseFuncAceArgs(arg)
        for _, arg in kwargs.items():
            allArgs += parseFuncAceArgs(arg)
        s += ', '.join(allArgs)
        
        # output the data
        logger.info("--[ {}: {} {}({}) ".format(config.COUNTER, indent, func.__name__, s))
        config.makerCallstack[makerCounter] = "--[ {:02d}: {} {}({})".format(config.COUNTER, indent, func.__name__, s)

        # call the actual function
        ret = func(*args, **kwargs)


        # What follows: Try to print ACE information of args+ret
        retType = str(type(ret))
        # dont show ret for AceRoute (no further processing possible)
        if 'AceRoute' in retType:
            return ret
        # If data is indexed, use that. 
        # If not, generate a new index
        if 'AceBytes' in retType or 'AceStr' in retType or 'AceFile' in retType:
            index = ret.index
        else:
            index = GetCounter()

        # output the results
        logger.info("--[ {}: {} -> {}".format(config.COUNTER, indent, index))
        config.makerCallstack[makerCounter] += " -> {}".format(index)

        # Dump content to files
        if not config.ENABLE_SAVING:
            return ret
        dumpDataToFile(index, func.__name__, ret, retType)

        return ret
    return wrapper


class AceRoute():
    def __init__(self, url: str, data: bytes, info: str = '', download: bool=False, downloadName: str='', downloadMime: str=None):
        self.url = url
        self.data = data
        self.info = info
        self.download = download
        self.downloadName = downloadName
        self.downloadMime = downloadMime


@DataTracker
def makeAceRoute(url: str, data: bytes, info: str = '', download: bool=False, downloadName: str='', downloadMime: str=None):
    aceRoute = AceRoute(url, data, info, download, downloadName, downloadMime)
    return aceRoute

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
