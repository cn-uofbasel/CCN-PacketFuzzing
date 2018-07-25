import pyndn.encoding as enc
from Generation.Package import TLVPackage
import random
from enum import Enum


class NDNPackages(Enum):
    Name = 0
    Interest = 1
    Data = 2
    LinkObject = 3


class CCNxPackages(Enum):
    Interest = 0
    ContentOject = 1


class PackageTypes(Enum):
    NDN = 0
    CCNx = 1


def makeBasicTLVPackage(name, type):
    len = randomLength()
    return TLVPackage(name, type, len)


def makeGenericNameComponent():
    return makeBasicTLVPackage("NameComponent", enc.Tlv.NameComponent)


def makeImplicitSha256DigestComponent():
    return makeBasicTLVPackage("ImplicitSha256DigestComponent", enc.Tlv.ImplicitSha256DigestComponent)


def makeSignatureType():
    return makeBasicTLVPackage("SignatureType", enc.Tlv.SignatureType)


def makeSignatureInfo():
    len = randomLength()
    stpackage = makeSignatureType()
    return TLVPackage("SignatureInfo", enc.Tlv.SignatureInfo, len, [stpackage])


def makeSignatureValue():
    return makeBasicTLVPackage("SignatureValue", enc.Tlv.SignatureValue)


def makeMetaInfo():
    return makeBasicTLVPackage("MetaInfo", enc.Tlv.MetaInfo)


def makePreference():
    return makeBasicTLVPackage("Preference", enc.Tlv.Link_Preference)


def makeDelegation():
    subpackages = []
    ppackage = makePreference()
    subpackages.append(ppackage)
    npackage = makeNamePacket()
    subpackages.append(npackage)
    length = randomLength(len(subpackages))
    return TLVPackage("Delegation", enc.Tlv.Link_Delegation, length, subpackages)


def makeLinkContent():
    cpackage = makeDelegation()
    length = randomLength(1)
    return TLVPackage("LinkContent", enc.Tlv.ContentType, length, [cpackage])


def makeNamePacket():
    gncpackage = makeGenericNameComponent()
    isdpackage = makeImplicitSha256DigestComponent()
    length = randomLength(2)
    npackage = TLVPackage("Name", enc.Tlv.Name, length, [gncpackage, isdpackage])
    return npackage


def makeInterestPacket():
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    length = randomLength(len(subpackages))
    ipackage = TLVPackage("Interest", enc.Tlv.Interest, length, subpackages)
    return ipackage


def makeDataPacket():
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    mipackage = makeMetaInfo()
    subpackages.append(mipackage)
    sipackage = makeSignatureInfo()
    subpackages.append(sipackage)
    svpackage = makeSignatureValue()
    subpackages.append(svpackage)
    length = randomLength(len(subpackages))
    datpackage = TLVPackage("Data", enc.Tlv.Data, length, subpackages)
    return datpackage


def makeLinkObject():
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    mipackage = makeMetaInfo()
    subpackages.append(mipackage)
    lcpackage = makeLinkContent()
    subpackages.append(lcpackage)
    sipackage = makeSignatureInfo()
    subpackages.append(sipackage)
    svpackage = makeSignatureValue()
    subpackages.append(svpackage)
    length = randomLength(len(subpackages))
    linkObject = TLVPackage("LinkObject", enc.Tlv.Data, length, subpackages)
    return linkObject


def randomLength(subpackes=1):
    random.random()
    return random.randint(0, 40 * subpackes)


def makeCCNxName():
    subpackages = []
    for x in range(random.randint(0, 20)):
        p = makeBasicTLVPackage("Name Segment", 0x0001)
        subpackages.append(p)
    length = randomLength(len(subpackages))
    return TLVPackage("Name", 0x0000, length, subpackages)


def makeKeyIdRestriciton():
    return makeBasicTLVPackage("KeyIdRestriction", 0x0002)


def makeContentObjectHashRestriciton():
    return makeBasicTLVPackage("ContentObjectHashRestriction", 0x0003)


def makeCCNxInterest():
    subpackages = []
    namep = makeCCNxName()
    subpackages.append(namep)
    x = random.randint(0, 3)
    if x % 2 is 1:
        kidp = makeKeyIdRestriciton()
        subpackages.append(kidp)
    if x > 1:
        cohrp = makeContentObjectHashRestriciton()
        subpackages.append(cohrp)
    length = randomLength(len(subpackages))
    return TLVPackage("Interest", 0x0001, length, subpackages)


def makePayloadType():
    return makeBasicTLVPackage("Payload", 0x0005)


def makeExpiriyTime():
    return TLVPackage("ExpiryTime", 0x0006, 8)


def makeCCNxContentObject():
    subpackages = []
    namep = makeCCNxName()
    subpackages.append(namep)
    x = random.randint(0, 3)
    if x % 2 is 1:
        ptp = makePayloadType()
        subpackages.append(ptp)
    if x > 1:
        extp = makeExpiriyTime()
        subpackages.append(extp)
    length = randomLength(len(subpackages))
    return TLVPackage("ContentOject", 0x0002, length, subpackages)


makePackage = {NDNPackages.Name: makeNamePacket(),
               NDNPackages.Data: makeDataPacket(),
               NDNPackages.Interest: makeInterestPacket(),
               NDNPackages.LinkObject: makeLinkObject(),
               CCNxPackages.Interest: makeCCNxInterest(),
               CCNxPackages.ContentOject: makeCCNxContentObject()
               }
