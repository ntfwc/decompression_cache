from subprocess import call

class BaseArchiveUnpacker(object):
	def __init__(self, archivePath):
		self.archivePath = archivePath

class TarUnpacker(BaseArchiveUnpacker):	
	def unpack(self, path):
		tarCall = ["tar", "-C", path, "-xf", self.archivePath]
		exitCode = call(tarCall)
		if exitCode != 0:
			raise Exception("tar returned nonezero exit code: %s" % exitCode)

class ZipUnpacker(BaseArchiveUnpacker):
	def unpack(self, path):
		unzipCall = ["unzip", "-q", self.archivePath, "-d", path]
		exitCode = call(unzipCall)
		if exitCode != 0:
			raise Exception("unzip returned nonezero exit code: %s" % exitCode)

import os.path

def _callAndPipeOutputToFile(callComponents, filePath):
	with open(filePath, "w") as f:
		exitCode = call(callComponents, stdout=f)
	return exitCode

def _getSimpleArchiveOutputFilePath(outputPath, archivePath, extensionToRemove):
	oldFileName = os.path.basename(archivePath)
	if oldFileName.endswith(extensionToRemove):
		newFileName = oldFileName[:-len(extensionToRemove)]
	else:
		newFileName = oldFileName
	return os.path.join(outputPath, newFileName)

class GzipUnpacker(BaseArchiveUnpacker):
	def unpack(self, path):
		newFilePath = _getSimpleArchiveOutputFilePath(path, self.archivePath, ".gz")
		zcatCall = ["zcat", self.archivePath]
		exitCode = _callAndPipeOutputToFile(zcatCall, newFilePath)
		if exitCode != 0:
			raise Exception("gunzip returned nonezero exit code: %s" % exitCode)

class XzUnpacker(BaseArchiveUnpacker):
	def unpack(self, path):
		newFilePath = _getSimpleArchiveOutputFilePath(path, self.archivePath, ".xz")
		xzcatCall = ["xzcat", self.archivePath]
		exitCode = _callAndPipeOutputToFile(xzcatCall, newFilePath)
		if exitCode != 0:
			raise Exception("xzcat returned nonezero exit code: %s" % exitCode)

def getUnpackerForArchive(archivePath):
	fileNameLowered = os.path.basename(archivePath).lower()
	if fileNameLowered.endswith(".tar.gz") or fileNameLowered.endswith(".tar.xz"):
		return TarUnpacker(archivePath)
	elif fileNameLowered.endswith(".zip"):
		return ZipUnpacker(archivePath)
	elif fileNameLowered.endswith(".gz"):
		return GzipUnpacker(archivePath)
	elif fileNameLowered.endswith(".xz"):
		return XzUnpacker(archivePath)
	raise Exception("Given unhandled file extension")
