
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

class TimeProvider(BaseChannelProvider):
    CHANNEL_NAME='periodic.time'

    def __init__(self, broker):
        super(TimeProvider, self).__init__(broker)

    def _handler(self, actor):
        lastSentTime = ''
        while True:
            test = time.strftime('%Y-%m-%d %H:%M %I:%M %p')
            if not(test==lastSentTime):
                self.publishMessage(test)
                print "Current Time: %s" % test
                lastSentTime = test
            time.sleep(1)    
