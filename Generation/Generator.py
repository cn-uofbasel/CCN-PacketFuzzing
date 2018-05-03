import pyndn.encoding as enc
import os
import random
from pyndn.util import Blob


class PacketMaker:

    def makeBasicBlob(type, len, data=0):
        encoder = enc.TlvEncoder()
        if data == 0:
            data = randomData(len)
        encoder.writeBuffer(data)
        len = randomLength(len)
        encoder.writeTypeAndLength(type, len)
        return Blob(encoder.getOutput())

    def makeGenericNameComponent(len, data=0):
        return makeBasicBlob(enc.Tlv.NameComponent, len, data)

    def makeImplicitSha256DigestComponent(len, data=0):
        return makeBasicBlob(enc.Tlv.ImplicitSha256DigestComponent, len, data)

    def makeNamePacket(len, data=0):
        blob = makeGenericNameComponent(int(len / 2), data)
        blob = Blob(blob.toBytes() + makeImplicitSha256DigestComponent(int(len / 2)).toBytes())
        return makeBasicBlob(enc.Tlv.Name, blob.__len__(), blob.toBytes())

    def makeInterestPacket(len, data=0):
        blob = makeNamePacket(len, data)
        return makeBasicBlob(enc.Tlv.Interest, blob.__len__(), blob.toBytes())

    def randomData(len):
        random.random()
        offset = random.randint(-(len - 1), 2 * len)
        return bytes(os.urandom(len + offset))

    def randomLength(len):
        random.random()
        return int(random.gauss(0, 2) + len)
