#!/usr/bin/python

import sys
import hashlib
import string

filen=open(sys.argv[1], 'rb')

for line in filen.xreadlines():
    line=line.strip()
    print hashlib.md5(line).hexdigest()

filen.close
