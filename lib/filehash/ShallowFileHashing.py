from FileMetaData import readFileMetaData
import struct

def __convertShallowFileDataToBinaryString(fileMetaData):
	name = fileMetaData.name
	size = fileMetaData.size
	lastModified = fileMetaData.lastModified
	return struct.pack("Ld" + str(len(name)) + "s", size, lastModified, name)

import hashlib

def __calculateMD5Hash(data):
	hashDigester = hashlib.md5()
	hashDigester.update(data)
	return hashDigester.digest()

def getShallowMD5Hash(filePath):
	fileMetaData = readFileMetaData(filePath)
	return __calculateMD5Hash(__convertShallowFileDataToBinaryString(fileMetaData))
