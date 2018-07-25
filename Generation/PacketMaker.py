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
        p = makeBasicTLVPackage("Name Segment", "T_NAME_SEGMENT")
        subpackages.append(p)
    length = randomLength(len(subpackages))
    return TLVPackage("Name", "T_NAME", length, subpackages)


def makeKeyIdRestriciton():
    return makeBasicTLVPackage("KeyIdRestriction", "T_KEYIDRESTR")


def makeContentObjectHashRestriciton():
    return makeBasicTLVPackage("ContentObjectHashRestriction", "T_OBJHASHRESTR")

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
    return TLVPackage("Interest", "T_INTEREST", length, subpackages)


def makePayloadType():
    return makeBasicTLVPackage("Payload", "T_PAYLDTYPE")


def makeExpiriyTime():
    return TLVPackage("ExpiryTime", "T_EXPIRY", 8)

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
    return TLVPackage("ContentOject", "T_OBJECT", length, subpackages)
    return


makePackage = {NDNPackages.Name: makeNamePacket(),
               NDNPackages.Data: makeDataPacket(),
               NDNPackages.Interest: makeInterestPacket(),
               NDNPackages.LinkObject: makeLinkObject(),
               CCNxPackages.Interest: makeCCNxInterest(),
               CCNxPackages.ContentOject: makeCCNxContentObject()
               }
