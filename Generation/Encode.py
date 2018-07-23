from pyndn.encoding import TlvEncoder
import random
from Logger import Logger
import os

fuzziness = 1

def setFuzziness(fuzz):
    global fuzziness
    fuzziness= fuzz

def encodePackage(package):
    global fuzziness
    logger = Logger.getLogger()
    logger.debug("encoding Package %s with fuzziness %d", package, fuzziness)
    encoder = TlvEncoder()
    subpackages = []
    len = 0
    if package.subpackages != None:
        subpackages = package.subpackages
        for p in reversed(subpackages):
            encoder.writeBuffer(encodePackage(p))
        len = encoder.getOutput().__len__()
        if (fuzziness < 2):
            package.len = len
    else:
        data = randomData(package.len)
        encoder.writeBuffer(data)
        len = data.__len__()
    package.rlen = len
    encoder.writeTypeAndLength(package.type, package.len)
    return encoder.getOutput()


def randomData(len):
    random.random()
    offset = 0
    if (fuzziness > 0):
        offset = random.randint(-len,len)
    return bytes(os.urandom(len+offset))
