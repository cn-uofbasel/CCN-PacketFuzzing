from pyndn.encoding import TlvEncoder
import random
import os
from Generation.Encoder import CCNxEncoder

fuzziness = 1


def setFuzziness(fuzz):
    global fuzziness
    fuzziness = fuzz


def encodeNDNPackage(package):
    global fuzziness
    encoder = TlvEncoder()
    len = 0
    if package.subpackages != None:
        for p in reversed(package.subpackages):
            encoder.writeBuffer(encodeNDNPackage(p))
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


def encodeCCNxSubpackages(package):
    encoder = CCNxEncoder()
    length = 0
    if package.subpackages is not None:
        for p in reversed(package.subpackages):
            encoder.writeMemoryView(encodeCCNxSubpackages(p))
        length = encoder.getOutput().__len__()
        if fuzziness < 2:
            package.len = length
    else:
        data = randomData(package.len)
        encoder.writeBuffer(data)
        length = data.__len__()
    package.rlen = length
    encoder.writeNumberFixedSize(package.len, 2)  # length
    encoder.writeNumberFixedSize(package.type, 2)  # type
    return encoder.getOutput()

def encodeCCNxPackage(package):
    global fuzziness
    encoder = CCNxEncoder()
    for p in reversed(package.subpackages):
        encoder.writeMemoryView(encodeCCNxSubpackages(p))
    if fuzziness < 2:
        package.len = encoder.getOutput().__len__()
    package.rlen = encoder.getOutput().__len__()
    encoder.writeNumberFixedSize(package.len, 2)  # message length
    encoder.writeNumberFixedSize(random.randint(0, 65535), 2)  # random message type
    length = encoder.__len__()
    encoder.writeNumberFixedSize(8, 1)  # header length
    encoder.writeNumberFixedSize(0, 1)  # flags
    if (package.name == 'ContentOject'):
        encoder.writeNumberFixedSize(0, 2)  # reserverd
        encoder.writeNumberFixedSize(length, 2)  # packetlength
        encoder.writeNumberFixedSize(package.type, 1)  # PT_CONTENT
    elif (package.name == 'Interest'):
        if random.randint(0, 1) == 1:
            encoder.writeNumberFixedSize(0, 1)  # reserved
            encoder.writeNumberFixedSize(random.randint(0, 255), 1)  # hoplimit
            encoder.writeNumberFixedSize(length, 2)  # packetlength
            encoder.writeNumberFixedSize(package.type, 1)  # PT_INTEREST
        else:
            encoder.writeNumberFixedSize(random.randint(1, 255), 1)  # return code
            encoder.writeNumberFixedSize(random.randint(0, 255), 1)  # hoplimit
            encoder.writeNumberFixedSize(length, 2)  # packet length
            encoder.writeNumberFixedSize(package.type + 1, 1)  # PT_RETURNc
    encoder.writeNumberFixedSize(1, 1)  # Version
    return encoder.getOutput()


def randomData(len):
    random.random()
    offset = 0
    if (fuzziness > 0):
        offset = random.randint(-len, len)
    return os.urandom(len + offset)
