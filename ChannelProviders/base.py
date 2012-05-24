
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


class BaseChannelProvider(object):
    CHANNEL_NAME = None

    def __init__(self, broker):
        if self.CHANNEL_NAME == None:
            raise NotImplementedError('Class %s does not set the CHANNEL_NAME to use.' % self.__class__.__name__)

        self.broker = broker
        self.broker.initChannel(self.CHANNEL_NAME)
        self.greenlet = Greenlet.spawn(self._handler, self)


    def publishMessage(self, message):
        self.broker.publish(self.CHANNEL_NAME, message)

    def _handler(self, actor):
        # self will be the greenlet
        print ('Class %s does not implement the _handler method.' % self.__class__.__name__)
        raise NotImplementedError('Class %s does not implement the _handler method.' % self.__class__.__name__)

    def shutdown(self):
        if self.greenlet:
            try:
                self.greenlet.kill()
            finally:
                pass

        pass

