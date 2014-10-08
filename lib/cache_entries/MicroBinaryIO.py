#Copyright (c) 2014 ntfwc

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import struct
from FileIO import readFile,writeFile
from os.path import getsize

def writeUnsignedLongLongToFile(filePath, longLong):
	data = struct.pack('Q', longLong)
	writeFile(filePath, data)

def writeDoubleToFile(filePath, double):
	data = struct.pack('d', double)
	writeFile(filePath, data)

def __checkFileSize(filePath, expectedSize):
	fileSize = getsize(filePath)
	if fileSize != expectedSize:
		raise IOError("Given file with unexpected file size: %s" % filePath)

def readUnsignedLongLongFromFile(filePath):
	__checkFileSize(filePath, 8)
	data = readFile(filePath)
	return struct.unpack('Q', data)[0]

def readDoubleFromFile(filePath):
	__checkFileSize(filePath, 8)
	data = readFile(filePath)
	return struct.unpack('d', data)[0]
