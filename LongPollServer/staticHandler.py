
#
#    MythTV-InfoScreen - long poll server giving MythTV information
#
#    Copyright (C) 2012 Andy Boff
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import mimetypes
from handler import RequestHandler
import os
import string

class StaticFileHandler(RequestHandler):
    def __init__(self, matchRe, baseDir):
        super(StaticFileHandler, self).__init__(matchRe)

        self.baseDir = baseDir
        mimetypes.init()

    def getHeaders(self, path, mo, environ):
        # mo should contain the path to the requested file.
        resultCode = "401 UNAVAILABLE"
        headers = [] 

        req = mo.group(1)

        if '../' in req:
            resultCode = "403 FORBIDDEN"
            headers.append(('Content-Type', 'text/html'))
        else:
            req = string.replace(req, '/', os.sep)
            fullPath = os.path.join(self.baseDir, req)
            fullFile = os.path.realpath(fullPath)

            if os.path.isdir(fullFile):
                resultCode = "403 FORBIDDEN"
                headers.append(('Content-Type', 'text/html'))
            elif os.path.isfile(fullFile):
                resultCode = "200 OK"
                (mimeType, encoding) = mimetypes.guess_type(fullFile)
                if not(mimeType):
                    mimeType = 'text/plain'
                headers.append(('Content-Type', mimeType))
                headers.append(('Content-Encoding', encoding))
            else:
                resultCode = "404 NOT FOUND"
                headers.append(('Content-Type', 'text/html'))

        return (resultCode, headers)


    def handleRequest(self, mo, body, params, environ):
        req = mo.group(1)

        if '../' in req:
            body.put('<html><body>')
            body.put('<h1>403 Forbidden</h1>')
            body.put('<p>You do not have permission to access this resource.</p>')
            body.put('</body></html>')
            body.put(StopIteration)
        else:
            req = string.replace(req, '/', os.sep)
            fullPath = os.path.join(self.baseDir, req)
            fullFile = os.path.realpath(fullPath)

            if os.path.isdir(fullFile):
                body.put('<html><body>')
                body.put('<h1>403 Forbidden</h1>')
                body.put('<p>You do not have permission to access this resource.</p>')
                body.put('</body></html>')
                body.put(StopIteration)
            elif os.path.isfile(fullFile):
                fh = open(fullFile, 'rb')
                body.put(fh.read())
                body.put(StopIteration)
                fh.close()
            else:
                body.put('<html><body>')
                body.put('<h1>404 Not Found</h1>')
                body.put('<p>The requested file was not found.</p>')
                body.put('</body></html>')
                body.put(StopIteration)

        return
