
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

from base import BaseChannelProvider
import time

class StateTableProvider(BaseChannelProvider):
    CHANNEL_NAME='state.misc'

    def __init__(self, broker, connectionProvider):
        super(StateTableProvider, self).__init__(broker)
        self.stateTable = connectionProvider
        self.stateTable.registerCallback(self._callback)

    def _handler(self, actor):
        # this isn't needed - all updates are driven by external sources
        pass

    def _callback(self, state):
        self.publishMessage(state)
