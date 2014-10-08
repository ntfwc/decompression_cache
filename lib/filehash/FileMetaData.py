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
