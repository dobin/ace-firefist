import logging
import io

logging.basicConfig(level=logging.INFO)
GlobalLog = None

def setupLogging():
    logger = logging.getLogger('basic_logger')
    logger.setLevel(logging.INFO)

    global GlobalLog
    GlobalLog = io.StringIO()
    ch = logging.StreamHandler(GlobalLog)
    ch.setLevel(logging.INFO)

    logger.addHandler(ch)
