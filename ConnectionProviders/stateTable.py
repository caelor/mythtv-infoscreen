
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

from base import BaseConnection

class StateTable(BaseConnection):
    def __init__(self):
        super(StateTable, self).__init__()
        self.state = {}

    def _handler(self, actor):
        # this isn't needed - all updates are driven by external sources
        pass

    def setState(self, key, value):
        self.state[key] = value
        self._notify(self.state)

