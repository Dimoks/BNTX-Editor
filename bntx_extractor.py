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

if getattr(sys, 'frozen', False):
    # If run as .exe
    exe_dir = os.path.dirname(sys.executable)
else:
    # If run as Python script
    exe_dir = os.path.dirname(os.path.abspath(__file__))

if exe_dir not in sys.path:
    sys.path.insert(0, exe_dir)

import bntx as BNTX
import globals

log_file = open('log.txt', 'a', encoding='utf-8')

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

outfolder = 'dds'

for i in range(bntx.texContainer.count):
    BFRESPath = os.path.dirname(btnx_file_path)
    texture = bntx.textures[i]
    name = texture.name.replace('\\', '_').replace('/', '_').replace(':', '_').replace('*', '_').replace(
            '?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
    ext = ''

    if (texture.format_ >> 8) in globals.ASTC_formats:
        outfolder = 'astc'
        ext = '.astc'
        if (bntx.texContainer.count > 1):
            file = os.path.join(BFRESPath, outfolder, bntx.name, name + ext)
        else:
            file = os.path.join(BFRESPath, outfolder, name + ext)

    else:
        outfolder = 'dds'
        ext = '.dds'
        if (bntx.texContainer.count > 1):
            file = os.path.join(BFRESPath, outfolder, bntx.name, name + ext)
        else:
            file = os.path.join(BFRESPath, outfolder, name + ext)

    if os.path.isfile(file):
        if (bntx.texContainer.count > 1):
            file = os.path.join(BFRESPath, outfolder, 'thumbs', bntx.name, name + ext)
        else:
            file = os.path.join(BFRESPath, outfolder, 'thumbs', name + ext)
        printer('Extracting thumb: ' + file + ' from ' + str(btnx_file_path))
        bntx.extract(i, BFRESPath, file, True)
    else:
        printer('Extracting: ' + file + ' from ' + str(btnx_file_path))
        bntx.extract(i, BFRESPath, file, True)

log_file.close()
