#!/usr/bin/env python
import os
import shutil
import re

shutil.copy('coverage.xml', 'coverage.xml.back')
lines = open('coverage.xml').readlines()
pat = re.compile(r'Generated')
cwd = os.getcwd()
fullpath = os.path.join(cwd, 'log4tailer')
fh = open('coverage.xml', 'w')
for line in lines:
    matched = pat.search(line)
    if matched:
        fh.write('<sources><source>'+cwd+'</source></sources>\n')
        continue
    fh.write(line)

