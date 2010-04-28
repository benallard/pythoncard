import os, re
import unittest

""" Greatly imspired from Dive into Python chap. 16.7 """

def allTests():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),"test"))
    print path
    files = os.listdir(path)
    print files
    test = re.compile("^test.+\.py$", re.IGNORECASE)
    files = filter(test.search, files)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    modules = []
    for module in moduleNames:
        module = "test.%s" % module
        print module
        modules.append(__import__(module))
    print modules
    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))


if __name__ == "__main__":
    unittest.main(defaultTest="allTests")
