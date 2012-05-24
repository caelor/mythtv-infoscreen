
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

class RequestHandler(object):
    def __init__(self, defaultRegex = None):
        super(RequestHandler, self).__init__()
        self.regex = defaultRegex

    def getMatchRegex(self):
        return self.regex

    def getHeaders(self, path, mo, environ):
        print "ERROR: Class %s does not implement getHeaders(path,mo)" % self.__class__.__name__
        return (
          "500 INTERNAL ERROR",
          [
            ('Content-Type', 'text/html')
          ]
        )

    def handleRequest(self, matchObject, body, params, environ):
        print "ERROR: Class %s does not implement handleRequest(mo,body)" % self.__class__.__name__
        body.put( '''<html><body>
                   <h1>500 Error</h1>
                   <p>The server generated an error. (Class %s does not implement handleRequest)</p>
                 </body></html>''' % self.__class__.__name__)
        body.put(StopIteration)

    def shutdown(self):
        pass

