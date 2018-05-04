import pyndn.encoding as enc
from Generation.Package import Package
import random


def makeBasicPackage(name, type):
    len = randomLength()
    return Package(name, type, len)


def makeGenericNameComponent():
    return makeBasicPackage("NameComponent", enc.Tlv.ValidityPeriod_NotAfter)


def makeImplicitSha256DigestComponent():
    return makeBasicPackage("ImplicitSha256DigestComponent", enc.Tlv.ImplicitSha256DigestComponent)


def makeSignatureType():
    return makeBasicPackage("SignatureType", enc.Tlv.SignatureType)


def makeSignatureInfo():
    len = randomLength()
    stpackage = makeSignatureType()
    return Package("SignatureInfo", enc.Tlv.SignatureInfo, len, [stpackage])


def makeSignatureValue():
    return makeBasicPackage("SignatureValue", enc.Tlv.SignatureValue)

def makeNamePacket():
    len = randomLength()
    gncpackage = makeGenericNameComponent()
    isdpackage = makeImplicitSha256DigestComponent()
    npackage = Package("Name", enc.Tlv.Name, len, [gncpackage, isdpackage])
    return npackage


def makeInterestPacket():
    len = randomLength()
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    ipackage = Package("Interest", enc.Tlv.Interest, len, subpackages)
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
    datpackage = Package("Data", enc.Tlv.Data, len, subpackages)
    return datpackage

def randomLength():
    random.random()
    random.sample
    return random.randint(0, 20)
