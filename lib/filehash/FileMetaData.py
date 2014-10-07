from os.path import basename
from os import stat

class FileMetaData(object):
	def __init__(self, name, size, lastModified, lastAccess, ctime):
		self.name = name
		self.size = size
		self.lastModified= lastModified
		self.lastAccess = lastAccess
		self.ctime = ctime


def readFileMetaData(filePath):
	name = basename(filePath)
	fileStats = stat(filePath)
	size = fileStats.st_size
	lastModified= fileStats.st_mtime
	lastAccess = fileStats.st_atime
	ctime = fileStats.st_ctime
	return FileMetaData(name, size, lastModified, lastAccess, ctime)
