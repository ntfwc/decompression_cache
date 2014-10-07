def readFile(filePath):
	with open(filePath) as f:
		return f.read()

def writeFile(filePath, data):
	with open(filePath, 'w') as f:
		f.write(data)
