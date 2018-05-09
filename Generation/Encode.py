from pyndn.encoding import TlvEncoder
import random
import os
import Packet_Fuzzing

def encodePackage(package):
    encoder = TlvEncoder()
    subpackages = []
    len = 0
    if package.subpackages != None:
        subpackages = package.subpackages
        for p in reversed(subpackages):
            encoder.writeBuffer(encodePackage(p))
        len = encoder.getOutput().__len__()
        if (Packet_Fuzzing.getFuzziness() < 2):
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
    if (Packet_Fuzzing.getFuzziness() > 0):
        offset = random.randint(-len,len)
    return bytes(os.urandom(len+offset))
