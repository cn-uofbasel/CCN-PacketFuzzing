import pyndn.encoding as enc
import os
from Generation.Package import Package
from pyndn.util import Blob
import random


def makeBasicPackage(name, type):
    len = randomLength()
    rlen = randomizeLength(len)
    return Package(name, type, len, rlen)


def makeGenericNameComponent():
    return makeBasicPackage("NameComponent", enc.Tlv.NameComponent)


def makeImplicitSha256DigestComponent():
    return makeBasicPackage("ImplicitSha256DigestComponent", enc.Tlv.ImplicitSha256DigestComponent)


def makeSignatureType():
    return makeBasicPackage("SignatureType", enc.Tlv.SignatureType)


def makeSignatureInfo():
    len = randomLength()
    stpackage = makeSignatureType()
    return Package("SignatureInfo", enc.Tlv.SignatureInfo, len, 0, [stpackage])


def makeSignatureValue():
    return makeBasicPackage("SignatureValue", enc.Tlv.SignatureValue)

def makeNamePacket():
    len = randomLength()
    gncpackage = makeGenericNameComponent()
    isdpackage = makeImplicitSha256DigestComponent()
    npackage = Package("Name", enc.Tlv.Name, len, 0, [gncpackage, isdpackage])
    return npackage


def makeInterestPacket():
    len = randomLength()
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    ipackage = Package("Interest", enc.Tlv.Interest, len, 0, subpackages)
    return ipackage


def makeDataPacket():
    len = randomLength()
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    sipackage = makeSignatureInfo()
    subpackages.append(sipackage)
    svpackage = makeSignatureValue()
    subpackages.append(svpackage)
    datpackage = Package("Data", enc.Tlv.Data, len, 0, subpackages)
    return datpackage


def randomData(len):
    random.random()
    offset = random.randint(-(len - 1), 2 * len)
    return bytes(os.urandom(len + offset))


def randomizeLength(len):
    random.random()
    return int(random.gauss(0, 2) + len)


def randomLength():
    random.random()
    return random.randint(0, 50)
