
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


from gevent import Greenlet

import mimetypes
from handler import RequestHandler
import os
import string
import time
import random

class StateTableHandler(RequestHandler):
    UPDATE_FREQUENCY=300

    def __init__(self, matchRe, stateTable):
        super(StateTableHandler, self).__init__(matchRe)

        self.stateTable = stateTable


    def getHeaders(self, path, mo, environ):
        # mo should contain the path to the requested file.
        resultCode = "200 OK"
        headers = [
          ('Content-Type', 'text/html')
        ] 

        return (resultCode, headers)


    def handleRequest(self, mo, body, params, environ):
        key = mo.group(1)
        value = mo.group(2)

        self.stateTable.setState(key, value)
        body.put('OK')
        body.put(StopIteration)

        return
