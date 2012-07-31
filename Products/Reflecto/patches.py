# -*- coding: utf-8 -*-

# checkValidId patch
from urllib import quote
from logging import getLogger
import os
from OFS.ObjectManager import checkValidId as checkValidIdBase
from zExceptions import BadRequest

log = getLogger('Reflecto')

def checkValidId(self, id, allow_dup=0):
    r""" Check for valid Zope id with basic encoding support

        >>> checkValidId('legal') is None
        True

        >>> checkValidId('%C3%B6l%20und%20m%C3%BCll') is None
        True

        >>> self.assertRaises(BadRequest, checkValidId, 'REQUEST')
        True

        >>> checkValidId(u'öl') is None
        True

        This are very special cases for the FHNW:

        >>> checkValidId('Thumbs.db')

        >>> checkValidId('~$test.doc')
    """
    if id == 'Thumbs.db':
        raise BadRequest
    elif id.startswith('~$'):
        raise BadRequest
    try:
        id = quote(id)
    except KeyError:
        id = quote(id.encode('utf-8'))
    # remove '%'-chars for original check.
    # We want to allow ids with it, since
    # we use it for quoting our umlauts
    id = id.replace('%', '')

    # do original check
    checkValidIdBase(self, id, allow_dup)

###############################################################################
# lnkparser patch
try:
    from hachoir_parser import createParser
    from hachoir_core.cmd_line import unicodeFilename
    from hachoir_parser.misc.lnk import LnkFile
    from hachoir_core.field import MissingField
    from hachoir_core.stream import InputStreamError

    WITH_LNK_PARSER = 1
    def lnkparse(reflectPath, filename):
        """ Return the target filename from a MS-widows link (URL format)
        """
        filename = unicodeFilename(filename)
        try:
            parser = createParser(filename)
            if parser is not None and isinstance(parser, LnkFile):
                #It is a "MS-Windows" link file
                try:
                    for field in parser: pass # trigger parsing
                    lnkpath = parser.getField('relative_path').value
                    # mount the complet target path,analyses if inside BasePath
                    if lnkpath.startswith('.\\'):
                        lnkpath = lnkpath[2:]
                    lnkpath = lnkpath.replace('\\','/')
                    filenamePath = os.path.dirname(filename)
                    allLnkpath = os.path.join(reflectPath, filenamePath, lnkpath)
                    allLnkpath = os.path.abspath(allLnkpath) #remove all ..\

                    if allLnkpath.startswith(reflectPath):
                        lnkpath = quote(lnkpath.encode('utf-8'))
                        return 'OK', lnkpath
                    else:
                        return 'ERROR_OUTREFLECTPATH', ''
                except MissingField:
                    # example: link to a network file
                    return 'ERROR_RELPATH', ''
            else:
                return 'NOT_LNKFILE', ''
        except InputStreamError:
            return 'NOT_PARSED', ''
except ImportError:
    WITH_LNK_PARSER = 0
    log.warn(('Hachoir parser not found! Parsing symlinks will not '
              'be available.'))
