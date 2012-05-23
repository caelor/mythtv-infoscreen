
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
from InfoPages import *

class InfoHandler(RequestHandler):
    def __init__(self, matchRe, broker, connections):
        super(InfoHandler, self).__init__(matchRe)

        self.pageHandlers = {
          '': self,
          'broker': BrokerInfoPage(broker),
          'state': StateTableInfoPage(connections['StateTable']),
          'mythtv': MythTVInfoPage(connections['MythTV'])
        }

    def getHeaders(self, path, mo, environ):
        # mo should contain the path to the requested file.
        page = mo.group(1)

        resultCode = "404 NOT FOUND"
        headers = [
          ('Content-Type', 'text/html')
        ] 

        if (page in self.pageHandlers.keys()):
            resultCode = "200 OK"

        return (resultCode, headers)


    def getExtraParams(self, path, mo):
        page = mo.group(1)
        if page in self.pageHandlers.keys():
            return self.pageHandlers[page].getExtraParams(path, mo)
        else:
            return None


    def handleRequest(self, mo, body, params, environ):
        page = mo.group(1)

        if page in self.pageHandlers.keys():
            return self.pageHandlers[page].handleRequest(mo, body, params)
        else:
            body.put(StopIteration)

        return
