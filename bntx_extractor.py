#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python version: sanity check

minimum = 3.4
import sys

currentRunningVersion = sys.version_info.major + (.1 * sys.version_info.minor)
if currentRunningVersion < minimum:
    errormsg = 'Please update your copy of Python to ' + str(minimum) + \
               ' or greater. Currently running on: ' + sys.version[:5]

    raise Exception(errormsg)

import os
import argparse
import pathlib
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import bntx as BNTX
import globals

log_file = open("log.txt", 'a', encoding='utf-8')

def printer(printing):
    
    print(str(datetime.now())+ ' ' + str(printing))
    log_file.write(str(datetime.now()) + ' ' + str(printing) + '\n')
    return

parser = argparse.ArgumentParser(description='Extract all textures from BNTX file.')
parser.add_argument('bntx_file', type=pathlib.Path, help='File to extract.')

args = parser.parse_args()

#print(args)

btnx_file_path = args.bntx_file

bntx = BNTX.File()
returnCode = bntx.readFromFile(btnx_file_path)

if returnCode:
    raise SystemExit('Error while opening the BNTX file.')

outfolder = "dds"

for i in range(bntx.texContainer.count):
    BFRESPath = os.path.dirname(btnx_file_path)
    texture = bntx.textures[i]
    name = texture.name.replace('\\', '_').replace('/', '_').replace(':', '_').replace('*', '_').replace(
            '?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
    
    if (texture.format_ >> 8) in globals.ASTC_formats:
        outfolder = "astc"
        if (bntx.texContainer.count > 1):
            file = os.path.join(BFRESPath, outfolder, bntx.name, name + '.astc')
        else:
            file = os.path.join(BFRESPath, outfolder, name + '.astc')
    
    else:
        outfolder = "dds"
        if (bntx.texContainer.count > 1):
            file = os.path.join(BFRESPath, outfolder, bntx.name, name + '.dds')
        else:
            file = os.path.join(BFRESPath, outfolder, name + '.dds')
    
    if os.path.isfile(file):
        printer(f"File exist: {file}")
        file = os.path.join(BFRESPath, outfolder, 'thumbs', name + '.dds')
        printer("Extracting thumb: " + os.path.split(btnx_file_path)[1])
        bntx.extract(i, BFRESPath, file, True)
    else:
        printer(f"File not exist: {file}")
        printer("Extracting: " + os.path.split(btnx_file_path)[1])
        bntx.extract(i, BFRESPath, 0, True)
        
log_file.close()
