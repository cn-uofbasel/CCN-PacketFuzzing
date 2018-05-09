from pyndn.encoding import TlvEncoder
import random
import os


def encodePackage(package):
    encoder = TlvEncoder()
    subpackages = []
    len = 0
    if package.subpackages != None:
        subpackages = package.subpackages
        for p in reversed(subpackages):
            encoder.writeBuffer(encodePackage(p))
        len = encoder.getOutput().__len__()
    else:
        data = randomData(package.len)
        encoder.writeBuffer(data)
        len = data.__len__()
    package.rlen = len
    encoder.writeTypeAndLength(package.type, package.len)
    return encoder.getOutput()


def randomData(len):
    random.random()
    offset = random.randint(0, 2 * len)
    return bytes(os.urandom(len + offset))
