
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
import uuid
import json

class RegisterHandler(RequestHandler):
    def __init__(self, matchRe, broker):
        super(RegisterHandler, self).__init__(matchRe)

        self.broker = broker


    def getHeaders(self, path, mo, environ):
        # mo should contain the path to the requested file.
        resultCode = "400 BAD REQUEST"
        headers = [
          ('Content-Type', 'text/html')
        ] 

        if (environ['REQUEST_METHOD'] == 'POST'):
            resultCode = "200 OK"
            headers = [
              ('Content-Type', 'application/json')
            ] 

        return (resultCode, headers)


    def handleRequest(self, mo, body, params, environ):
        body.put(' ' * 1000)
        if (environ['REQUEST_METHOD'] == 'POST'):
            ident = str(uuid.uuid4())
            self.broker.initEndpoint(ident, mo.group(1))
            print "N %s: Registered (%s)" % (ident, mo.group(1))
            res = {
              'status': 'success',
              'uuid': ident
            }
            body.put(json.dumps(res))
        else:
            body.put('Invalid')

        body.put(StopIteration)

        return
