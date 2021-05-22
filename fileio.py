# Return lines from a file
def getFileLines(file):
    f = open(file, "r")
    lines = f.readlines()
    f.close
    return lines