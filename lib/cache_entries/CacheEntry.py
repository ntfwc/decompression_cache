#Copyright (C) 2014 ntfwc

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

def calculateDirSize(directory):
	if not os.path.isdir(directory):
		raise IOError("content dir '%s' does not exist" % directory)
	size = 0
	for dirpath, dirnames, filenames in os.walk(directory):
		for filename in filenames:
			path = os.path.join(dirpath, filename)
			size += os.path.getsize(path)
	return size

from MicroBinaryIO import writeUnsignedLongLongToFile, writeDoubleToFile

CONTENT_DIR = "content"
SIZE_FILE_NAME = "size.bin"
LAST_ACCESSED_FILE_NAME = "lastAccessed.bin"

CACHE_ENTRY_METADATA_SIZE=16

from time import time

class CacheEntry(object):
	def __init__(self, path, size=None, lastAccessed=None):
		self.path = path
		self.contentPath = os.path.join(self.path, CONTENT_DIR)
		self.size = size
		self.lastAccessed = lastAccessed
	
	def __calculateSize(self):
		return calculateDirSize(self.contentPath)
		
	def __recordSize(self):
		sizeFilePath = os.path.join(self.path, SIZE_FILE_NAME)
		writeUnsignedLongLongToFile(sizeFilePath, self.size)
	
	def updateSize(self):
		calculatedSize = self.__calculateSize()
		if self.size != calculatedSize:
			self.size = calculatedSize
			self.__recordSize()
	
	def __recordLastAccessed(self):
		lastAccessedFilePath = os.path.join(self.path, LAST_ACCESSED_FILE_NAME)
		writeDoubleToFile(lastAccessedFilePath, self.lastAccessed)
	
	def updateLastAccessed(self):
		self.lastAccessed = time()
		self.__recordLastAccessed()
	
	def getKey(self):
		return os.path.basename(self.path)
	
	def getTotalSize(self):
		return self.size + CACHE_ENTRY_METADATA_SIZE


def __verifyItems(entryPath):
	items = os.listdir(entryPath)
	if CONTENT_DIR not in items or SIZE_FILE_NAME not in items or LAST_ACCESSED_FILE_NAME not in items:
		raise IOError("Cache Entry does not contain expected file and directories")

from MicroBinaryIO import readUnsignedLongLongFromFile, readDoubleFromFile

def readCacheEntry(entryPath):
	__verifyItems(entryPath)
	sizeFilePath = os.path.join(entryPath, SIZE_FILE_NAME)
	size = readUnsignedLongLongFromFile(sizeFilePath)
	lastAccessedFilePath = os.path.join(entryPath, LAST_ACCESSED_FILE_NAME)
	lastAccessed = readDoubleFromFile(lastAccessedFilePath)
	return CacheEntry(entryPath, size, lastAccessed)


def createCacheEntry(entryPath, dataUnpacker):
	contentDir = os.path.join(entryPath, CONTENT_DIR)
	os.mkdir(contentDir)
	dataUnpacker.unpack(contentDir)
	cacheEntry = CacheEntry(entryPath)
	cacheEntry.updateSize()
	cacheEntry.updateLastAccessed()
	return cacheEntry
