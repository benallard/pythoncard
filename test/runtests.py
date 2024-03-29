import os, re, sys
import unittest

""" Greatly imspired from Dive into Python chap. 16.7 """

sys.path = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))] + sys.path

def allTests():
    path = os.path.abspath(os.path.dirname(__file__))
    files = os.listdir(path)
    print(files)
    test = re.compile("^test.+\.py$", re.IGNORECASE)
    files = filter(test.search, files)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    print(files)
    moduleNames = map(filenameToModuleName, files)
    print(moduleNames)
    modules = map(__import__, moduleNames)
    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))


if __name__ == "__main__":
    unittest.main(defaultTest="__main__.allTests", module=None)
