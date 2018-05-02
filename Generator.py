import pyndn.encoding as enc
import os
import random
import pyndn.util as util

def makeBasicBlob(type, len, data=0):
    encoder = enc.TlvEncoder()
    if data == 0:
        data = randomData(len)
    encoder.writeBuffer(data)
    encoder.writeTypeAndLength(type, len)
    return util.Blob(encoder.getOutput())

def makeGenericNameComponent(len, data=0):
    return makeBasicBlob(enc.Tlv.NameComponent, len, data)

def makeImplicitSha256DigestComponent(len, data=0):
    return makeBasicBlob(enc.Tlv.ImplicitSha256DigestComponent, len, data)


def makeNamePacket(len, data=0):
    blob = makeGenericNameComponent(len, data)
    blob = util.Blob(blob.toBytes() + makeImplicitSha256DigestComponent(3).toBytes())
    return makeBasicBlob(enc.Tlv.Name,len,blob.toBytes())


def makeInterestPacket(len, data=0):
    blob = makeNamePacket(len, data)
    return makeBasicBlob(enc.Tlv.Interest,len,blob.toBytes())


def randomData(len):
    random.random()
    offset = random.randint(-(len - 1), 2 * len)
    return bytes(os.urandom(len + offset))
