## Results

CCN-Lite:

900 Packages sent, incorrectness level 0,1,2 --> packages will be ignored if not interpretable

-> works fine.

Future test: 
    -remove non-optional packages from ndn packet
    -also send only a sublevel packet

PiCN:

Bug: MetaInfo optional since NDN packet version 0.3, but PiCN tries to decode meta info even if no meta info is in the
packet --> error not caught --> parser crashes, following packages received but no more decoding.

Interestpackages: 900 Packages sent, correctly ignored false info, no errors raised.


