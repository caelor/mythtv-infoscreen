
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

import time
from gevent import queue

class Registration:
    # This class represents a single channel registration, for a single
    # endpoint. It carries a copy of the channel messages, destined for the
    # endpoint. The channel class provides the one channel->many registrations
    # mapping, and the endpoint class provides the many registrations->one
    # endpoint mapping.

    def __init__(self):
        self.queue = queue.Queue()
        self.unregistered = False

    def isStale(self):
        return self.unregistered

    def getQueue(self):
        return self.queue

    def unregister(self):
        # called by the Endpoint on destroy/unsubscribe.
        # indicates to the channel to destroy this registration
        self.unregistered = True
