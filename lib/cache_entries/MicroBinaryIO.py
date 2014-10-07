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
