#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BNTX Editor
# Version 0.3
# Copyright © 2018 AboodXD

# This file is part of BNTX Editor.

# BNTX Editor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# BNTX Editor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Python version: sanity check
minimum = 3.4
import sys

# currentRunningVersion = sys.version_info.major + (.1 * sys.version_info.minor)
# if currentRunningVersion < minimum:
#     errormsg = 'Please update your copy of Python to ' + str(minimum) + \
#                ' or greater. Currently running on: ' + sys.version[:5]

#     raise Exception(errormsg)

import os.path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtWidgets
import time
import traceback

import bntx as BNTX
import globals

global bntx
bntx = BNTX.File()

def saveToPng(name, texture):
	if texture.format_ in [0x101, 0x201, 0x301, 0x401, 0x501, 0x601, 0x701,
									0x801, 0x901, 0xb01, 0xb06, 0xc01, 0xc06, 0xe01,
									0x1a01, 0x1a06, 0x1b01, 0x1b06, 0x1c01, 0x1c06,
									0x1d01, 0x1d02, 0x1e01, 0x1e02, 0x3b01] and texture.dim == 2:

		global bntx
		result, _, _ = bntx.rawData(texture)

		if texture.format_ == 0x101:
				data = result[0]

				format_ = 'la4'
				bpp = 1

		elif texture.format_ == 0x201:
				data = result[0]

				format_ = 'l8'
				bpp = 1

		elif texture.format_ == 0x301:
				data = result[0]

				format_ = 'rgba4'
				bpp = 2

		elif texture.format_ == 0x401:
				data = result[0]

				format_ = 'abgr4'
				bpp = 2

		elif texture.format_ == 0x501:
				data = result[0]

				format_ = 'rgb5a1'
				bpp = 2

		elif texture.format_ == 0x601:
				data = result[0]

				format_ = 'a1bgr5'
				bpp = 2

		elif texture.format_ == 0x701:
				data = result[0]

				format_ = 'rgb565'
				bpp = 2

		elif texture.format_ == 0x801:
				data = result[0]

				format_ = 'bgr565'
				bpp = 2

		elif texture.format_ == 0x901:
				data = result[0]

				format_ = 'la8'
				bpp = 2

		elif (texture.format_ >> 8) == 0xb:
				data = result[0]

				format_ = 'rgba8'
				bpp = 4

		elif (texture.format_ >> 8) == 0xc:
				data = result[0]

				format_ = 'bgra8'
				bpp = 4

		elif texture.format_ == 0xe01:
				data = result[0]

				format_ = 'bgr10a2'
				bpp = 4

		elif (texture.format_ >> 8) == 0x1a:
				data = BNTX.bcn.decompressDXT1(result[0], texture.width, texture.height)

				format_ = 'rgba8'
				bpp = 4

		elif (texture.format_ >> 8) == 0x1b:
				data = BNTX.bcn.decompressDXT3(result[0], texture.width, texture.height)

				format_ = 'rgba8'
				bpp = 4

		elif (texture.format_ >> 8) == 0x1c:
				data = BNTX.bcn.decompressDXT5(result[0], texture.width, texture.height)

				format_ = 'rgba8'
				bpp = 4

		elif (texture.format_ >> 8) == 0x1d:
				data = BNTX.bcn.decompressBC4(result[0], texture.width, texture.height, 0 if texture.format_ & 3 == 1 else 1)

				format_ = 'rgba8'
				bpp = 4

		elif (texture.format_ >> 8) == 0x1e:
				data = BNTX.bcn.decompressBC5(result[0], texture.width, texture.height, 0 if texture.format_ & 3 == 1 else 1)

				format_ = 'rgba8'
				bpp = 4

		elif texture.format_ == 0x3b01:
				data = result[0]

				format_ = 'bgr5a1'
				bpp = 2

		data = BNTX.dds.formConv.torgba8(texture.width, texture.height, bytearray(data), format_, bpp, texture.compSel)
		img = QImage(data, texture.width, texture.height, QImage.Format_RGBA8888)

		img.save(name)
	else:
		pass

import sys
def main():
	global bntx

	print(" start converting ")
	for filename in sys.argv[1:]:
		print(filename)
		returnCode = bntx.readFromFile(filename)
		BFRESPath = os.path.abspath(filename)
		if returnCode:
			return False
		else:
			for texture in bntx.textures:
				print(BFRESPath + texture.name + ".png")
				saveToPng( BFRESPath + texture.name + ".png", texture)

	print(" end converting ")

if __name__ == '__main__':
	main()
