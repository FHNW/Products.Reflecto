# -*- coding: utf-8 -*-
from zope.interface import implements
from Products.Reflecto.interfaces import IReflector
import Acquisition
import os.path
import sys

samplesPath=os.path.join(sys.modules["Products.Reflecto.tests"].__path__[0],
                        "samples")


class MockReflector(Acquisition.Implicit):
    implements(IReflector)

    _at_uid = '35b46994-7454-4efa-8888-54c9b068230b'

    def getFilesystemPath(self):
        return samplesPath

# + patch
import shutil

umlautdirs = [
 [u'öl und müll'],
 [u'geänderte Dokumente.txt'],
 [u'Verknüpfung OUT BasePath.lnk'],              
 ['l und mll', 'deep', u'ölsardine'],
 ['l und mll', 'Direktion, Stab', u'11 Ausbildung übergreifend'],
 ['l und mll', u'Pädagogische Hochschule'], 
 ['l und mll', 'Pdagogische Hochschule', u'11 Ausbildung übergreifend.lnk'],
 ['l und mll', u'mönster file.txt'],
 ['l und mll', u'Verknüpfung mit mönster file.txt.lnk'],
]

def setupUmlautDirs():
    revud = umlautdirs[:]
    revud.reverse()
    for path in revud:
        asciiname = path[-1].encode('ascii', 'ignore')
        utf8name = path[-1].encode('utf-8')
        asciipath = [samplesPath] + path[:-1] + [asciiname]
        utf8path = [samplesPath] + path[:-1] + [utf8name]
        try:
            shutil.move(os.path.join(*asciipath),
                        os.path.join(*utf8path))
        except IOError:
            print "failure when setup umlaut dirs!"
    
def teardownUmlautDirs():
    for path in umlautdirs:
        asciiname = path[-1].encode('ascii', 'ignore')
        utf8name = path[-1].encode('utf-8')
        asciipath = [samplesPath] + path[:-1] + [asciiname]
        utf8path = [samplesPath] + path[:-1] + [utf8name]
        try:
            shutil.move(os.path.join(*utf8path),
                        os.path.join(*asciipath))
        except IOError:
            print "failure when tear down umlaut dirs!"

# - patch
