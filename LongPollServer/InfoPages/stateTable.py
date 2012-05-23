
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

import string
import pprint

class StateTableInfoPage:
    def __init__(self, stateTable):
        self.stateTable = stateTable 

    def getExtraParams(self, path, mo):
        return self.stateTable

    def handleRequest(self, mo, body, extra):
        body.put('<html><body>')
        body.put('<h1>State Table status</h1>')
        body.put('<pre>')
        body.put(pprint.pformat(self.stateTable.state, 4))
        body.put('</pre>')
        body.put('</body></html>')
        body.put(StopIteration)
        pass

