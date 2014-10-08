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

from cache_entries.CacheEntry import readCacheEntry, createCacheEntry
from Unpackers import getUnpackerForArchive
import os
from shutil import rmtree

def exceptionToString(exception):
	return exception.__class__.__name__ + " : " + str(exception)

def listFolders(directory):
	itemNames = os.listdir(directory)
	folderNames = []
	for itemName in itemNames:
		itemPath = os.path.join(directory, itemName)
		if os.path.isdir(itemPath):
			folderNames.append(itemName)
	
	return folderNames

from operator import attrgetter
from sys import stderr

class Cache(object):	
	def __readOrRemoveCacheEntry(self, entryName):
		entryPath = os.path.join(self.cacheFolder, entryName)
		try:
			cacheEntry = readCacheEntry(entryPath)
			self.cacheEntryDict[entryName] = cacheEntry
		except Exception, e:
			stderr.write("Warning: " + exceptionToString(e) + '\n')
			stderr.write("Removed entry: %s\n" % entryPath)
			rmtree(entryPath)
	
	def __readCacheEntries(self):
		self.cacheEntryDict = {}
		entryNames = listFolders(self.cacheFolder)
		for entryName in entryNames:
			self.__readOrRemoveCacheEntry(entryName)
	
	def __init__(self, cacheFolder, targetSize):
		self.cacheFolder = cacheFolder
		self.targetSize = targetSize
		self.__readCacheEntries()
	
	def __createNewCacheEntry(self, key, archivePath):
		newEntryPath = os.path.join(self.cacheFolder, key)
		os.mkdir(newEntryPath)
		
		try:
			unpacker = getUnpackerForArchive(archivePath)
			newCacheEntry = createCacheEntry(newEntryPath, unpacker)
			self.cacheEntryDict[key] = newCacheEntry
			return newCacheEntry
		except Exception, e:
			rmtree(newEntryPath)
			raise e
		
	def __getCurrentCacheSize(self):
		totalSize = 0
		for cacheEntry in self.cacheEntryDict.values():
			totalSize += cacheEntry.getTotalSize()
		return totalSize
	
	def __getOldCacheEntriesSortedByLastAccess(self, newCacheEntry):
		cacheEntries = self.cacheEntryDict.values()
		cacheEntries.remove(newCacheEntry)
		return sorted(cacheEntries, key=attrgetter("lastAccessed"))
	
	def __removeCacheEntry(self, cacheEntry):
		key = cacheEntry.getKey()
		del self.cacheEntryDict[key]
		entryPath = os.path.join(self.cacheFolder, key)
		rmtree(entryPath)
	
	def __trimCacheTowardTargetSize(self, newCacheEntry):
		currentSize = self.__getCurrentCacheSize()
		if currentSize > self.targetSize:
			oldCacheEntryList = self.__getOldCacheEntriesSortedByLastAccess(newCacheEntry)
			for entry in oldCacheEntryList:
				currentSize -= entry.getTotalSize()
				self.__removeCacheEntry(entry)
				if currentSize <= self.targetSize:
					return
	
	def recallOrCreateEntryAndGetContentPath(self, key, archivePath):
		if key in self.cacheEntryDict:
			cacheEntry = self.cacheEntryDict[key]
			cacheEntry.updateLastAccessed()
			return cacheEntry.contentPath
		
		cacheEntry = self.__createNewCacheEntry(key, archivePath)
		self.__trimCacheTowardTargetSize(cacheEntry)
		return cacheEntry.contentPath
