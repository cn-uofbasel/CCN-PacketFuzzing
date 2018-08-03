from pyndn.encoding import TlvEncoder
import random
from Logger import Logger
import os
from Generation.Encoder import CCNxEncoder

"""
Module to encode packetstruktures to bytemessages.

Each supported packettype has at least one main encoding function name encode'paketformat name' package.
These methods take a structure from the package module and convert them according to the packetprotocoll into a memoryview of a bytearray.
This memoryview is then send to the active parser. 
"""
fuzziness = 1


def setFuzziness(fuzz):
    """defines the fuzziness for all encode functions"""
    global fuzziness
    fuzziness = fuzz


def encodeNDNPackage(package):
    """
    Encodes a NDNPackage recursively into bits

    :param package: a Package.TLVPackage representing a NDNPackage. All length values except the ones on the deepest layer are ignored and updated according to fuzziness level.
    :return: a memoryview of a bytearray. The actual NDNPackage

    The packagestructure is traversed in backwards depth-first order to fill to bytearry of the encoder from back to front.
    """
    global fuzziness
    logger = Logger.getLogger()
    logger.debug("encoding Package %s with fuzziness %d", package, fuzziness)
    encoder = TlvEncoder()
    len = 0
    if package.subpackages != None:  # package payload is a TLV itself
        for p in reversed(package.subpackages):
            encoder.writeBuffer(encodeNDNPackage(p))
        len = encoder.getOutput().__len__()
        if (fuzziness < 2):
            package.len = len
    else:  # recursion end
        data = randomData(package.len)
        encoder.writeBuffer(data)
        len = data.__len__()
    package.rlen = len
    encoder.writeTypeAndLength(package.type, package.len)
    return encoder.getOutput()


def _encodeCCNxSubpackages(package):
    encoder = CCNxEncoder()
    length = 0
    if package.subpackages is not None:  # package payload is a TLV itself
        for p in reversed(package.subpackages):
            encoder.writeMemoryView(_encodeCCNxSubpackages(p))
        length = encoder.getOutput().__len__()
        if fuzziness < 2:
            package.len = length
    else:  # recursion end
        data = randomData(package.len)
        encoder.writeByteArray(data)
        length = data.__len__()
    package.rlen = length
    encoder.writeNumberFixedSize(package.len, 2)  # length
    encoder.writeNumberFixedSize(package.type, 2)  # type
    return encoder.getOutput()

def encodeCCNxPackage(package):
    """
        Encodes a CCNxPackage partly recursive into bits

        :param package: a Package.TLVPackage representing the TLV part of a CCNx package. All length values except the ones on the deepest layer are ignored and updated according to fuzziness level.
        :return: a memoryview of a bytearray. The actual NDNPackage

        The packagestructure is traversed in backwards depth-first order to fill to bytearry of the encoder from back to front. Then the fixed header is added according to the packet.name field.
        """
    global fuzziness
    # make message
    encoder = CCNxEncoder()
    for p in reversed(package.subpackages):
        encoder.writeMemoryView(_encodeCCNxSubpackages(p))
    if fuzziness < 2:
        package.len = encoder.getOutput().__len__()
    package.rlen = encoder.getOutput().__len__()
    encoder.writeNumberFixedSize(package.len, 2)  # message length
    encoder.writeNumberFixedSize(package.type, 2)  # random message type
    length = encoder.__len__()
    encoder.writeNumberFixedSize(8, 1)  # header length
    encoder.writeNumberFixedSize(0, 1)  # flags

    # add fixed header
    if (package.name == 'ContentOject'):
        encoder.writeNumberFixedSize(0, 2)  # reserved
        encoder.writeNumberFixedSize(length, 2)  # packetlength
        encoder.writeNumberFixedSize(1, 1)  # PT_CONTENT
    elif (package.name == 'Interest'):
        if random.randint(0, 1) == 1:
            encoder.writeNumberFixedSize(0, 1)  # reserved
            encoder.writeNumberFixedSize(random.randint(0, 255), 1)  # hoplimit
            encoder.writeNumberFixedSize(length, 2)  # packetlength
            encoder.writeNumberFixedSize(0, 1)  # PT_INTEREST
        else:
            encoder.writeNumberFixedSize(random.randint(1, 255), 1)  # return code
            encoder.writeNumberFixedSize(random.randint(0, 255), 1)  # hoplimit
            encoder.writeNumberFixedSize(length, 2)  # packet length
            encoder.writeNumberFixedSize(2, 1)  # PT_RETURN
    encoder.writeNumberFixedSize(1, 1)  # Version
    return encoder.getOutput()


def randomData(len):
    """random length manipulation on fuzzing levels 1 and 2"""
    random.random()
    offset = 0
    if (fuzziness > 0):
        offset = random.randint(-len, len)
    return os.urandom(len + offset)
