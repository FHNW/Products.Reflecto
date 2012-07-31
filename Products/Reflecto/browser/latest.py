# -*- coding: utf-8 -*-
###############################################################################
# $Copy$
###############################################################################
""" Browser views for filesystem reflector


$Id: latest.py 5189 2008-04-24 15:38:40Z thomasmichael.gross $
"""
__docformat__ = 'reStructuredText'
__author__  = 'Tom Gross <thomasmichael.gross@fhnw.ch>'

# python imports
import csv
from os.path import join
from urllib import quote

# zope2 imports
from Products.Five import BrowserView
from DateTime import DateTime

# zope3 imports

# plone imports

# third party imports

# own factory imports

###############################################################################

class excel_dollar(csv.excel):
    r""" A csv dialect using '$' as delimiter

        >>> from cStringIO import StringIO
        >>> import csv
        >>> csvfile = StringIO()
        >>> writer = csv.writer(csvfile, dialect="excel_dollar")
        >>> writer.writerow(['hello', 'world'])

        >>> csvfile.getvalue()
        'hello$world\r\n'

        >>> writer.writerow(['special $ char', 'foo', 'bar'])
        >>> csvfile.getvalue()
        'hello$world\r\n"special $ char"$foo$bar\r\n'
    """
    delimiter = '$'

csv.register_dialect('excel_dollar', excel_dollar)

class LatestChangesView(BrowserView):
    """ Give a list of latest changed documents.

        We have a file called 'changesfile' in the root of the
        folder we reflect.
        This file is structured like:

        # a comment is marked with a '#' as first char of a line
        17.04.2007$Services\Example.pdf$This is an example document

        There are three fields: date/document (including full path)/description

        The file is parsed and returned as dictionary with the
        following keys/values:

          date: date
          document: document (just the name of the document)
          link: document (including full path)
          description: description

        Dates not parsable are returned as 01.01.1970..
    """

    changesfile = u'geänderte Dokumente.txt'

    def entries(self):
        """ Read data, parse it and return as dict """
        try:
            reader = csv.reader(open(join(self.context.getFilesystemPath(),
                                          self.changesfile), 'rb'),
                                'excel_dollar')
        except IOError:
            message = quote('Datei "%s" wurde nicht gefunden!' %
                                    self.changesfile.encode('utf-8'))
            url = '%s/plfng_view?portal_status_message=%s!' % (
                    self.context.absolute_url(), message)
            self.request.response.redirect(url)
            return
        result = []
        for row in reader:
            if not row or len(row) != 3 or row[0].startswith('#'):
                continue

            try:
                date = DateTime(row[0])
            except DateTime.DateError:
                date = DateTime('01.01.1970')

            result.append(dict(
                date=date,
                link=quote(row[1].replace('\\', '/')),
                document=row[1][row[1].rfind('\\')+1:],
                description=row[2]))
        return result

# EOF
