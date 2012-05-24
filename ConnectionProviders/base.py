
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
from MythTV import MythBE, FileOps, Program, BECache, BEEventConnection, MythDB
import re

class BaseConnection(object):
    def __init__(self):
        self.messageCallbacks = []

    def _notify(self, param):
        for cb in self.messageCallbacks:
            cb(param)

    def registerCallback(self, callback):
        self.messageCallbacks.append(callback)

    def deregisterCallback(self, callback):
        self.messageCallbacks.remove(callback)

    def shutdown(self):
        pass
