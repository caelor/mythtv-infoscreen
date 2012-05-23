
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

from handler import RequestHandler

class RedirectHandler(RequestHandler):
    def __init__(self, matchRe, destUrl):
        super(RedirectHandler, self).__init__(matchRe)

        self.destUrl = destUrl

    def getHeaders(self, path, mo, environ):
        # mo should contain the path to the requested file.
        resultCode = "302 REDIRECT"
        headers = [
          ('Location', self.destUrl)
        ] 

        return (resultCode, headers)


    def handleRequest(self, mo, body, params, environ):
        body.put(StopIteration)

        return
