#!/usr/env python3

import sys

[SurnameFN,GivenNFN]=sys.argv[1:2]

for Surname in open(SurnameFN).split('\n'):
    for GivenName in open(GivenNameFN).split('\n'):
        print(Surname+' '+GivenName)
