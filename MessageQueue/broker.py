
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
import time
import string

from channel import Channel
from endpoint import Endpoint

class MessageBroker:
    # how frequently the maintenance thread should run.
    MAINTENANCE_TIMEOUT=10
    SYSTEM_CHANNEL='system.status'

    def __init__(self):
        self.channels = {}
        self.endpoints = {}
        self.maint = Greenlet.spawn(self._maintenanceLoop, self)
        self.publish(MessageBroker.SYSTEM_CHANNEL, 'Message Broker Startup')
        pass


    def _maintenanceLoop(self, actor):
        # self will be the greenlet object
        while True:
            for ident in actor.endpoints.keys():
                details = actor.getEndpointDetails(ident)
                #print "I %s: %s" % (ident, details['desc'])
                #print "  %s: %d messages queued, last request %s seconds ago (Client connected: %s)" % (ident, details['queueSize'], details['age'], details['isWaiting'])
                #print "  %s: Subscribed to %s" % (ident, string.join(details['subscriptions'], ', '))
                if actor.endpoints[ident].isStale():
                    actor.publish(MessageBroker.SYSTEM_CHANNEL, 'Removing stale endpoint %s (%s)' % (ident, details['desc']))
                    print "D %s: Removing stale endpoint (%s)" % (ident, details['desc'])
                    actor.endpoints[ident].finish()
                    del actor.endpoints[ident]
                    
            time.sleep(MessageBroker.MAINTENANCE_TIMEOUT)


    def _createChannel(self, channel):
        if not(channel == MessageBroker.SYSTEM_CHANNEL):
            self.publish(MessageBroker.SYSTEM_CHANNEL, 'Added channel %s' % channel)
        self.channels[channel] = Channel(channel)

    def _createEndpoint(self, ident, description = 'Unknown'):
        self.publish(MessageBroker.SYSTEM_CHANNEL, 'Added endpoint %s (%s)' % (ident, description))
        self.endpoints[ident] = Endpoint(self, ident, description)

    def publish(self, channel, message):
        if not(channel in self.channels.keys()):
            self._createChannel(channel)

        self.channels[channel].publish(message)


    def initChannel(self, channel):
        if not(channel in self.channels.keys()):
            self._createChannel(channel)

    def initEndpoint(self, ident, description):
        if not(ident in self.endpoints.keys()):
            self._createEndpoint(ident, description)

    def getEndpoint(self, ident, canCreate = True):
        if not(ident in self.endpoints.keys()):
            if canCreate:
                self._createEndpoint(ident)
            else:
                return None

        return self.endpoints[ident]


    def getChannels(self):
        return self.channels.keys()

    def getChannel(self, channel):
        if (channel in self.channels.keys()):
            return self.channels[channel]
        else:
            return None

    def getEndpoints(self):
        return self.endpoints.keys()

    def getChannelDetails(self, channel):
        if not(channel in self.channels.keys()):
            return None

        c = self.channels[channel]
        return {
          'registrations': c.getRegistrationCount(),
          'messages': c.getMessageCount()
        }

    def getEndpointDetails(self, ident):
        if not(ident in self.endpoints.keys()):
            return None

        e = self.endpoints[ident]
        return {
          'desc': e.getDescription(),
          'subscriptions': e.getSubscriptions(),
          'queueSize': e.getQueueSize(),
          'age': e.getAge(),
          'isWaiting': e.getWaiting()
        }

    def forceUpdate(self, ident, channel):
        if channel in self.channels.keys():
            self.channels[channel].forceUpdate()
            return True
        else:
            return False

    def setDebug(self, channel, state):
        if channel in self.channels.keys():
            self.channels[channel].setDebug(state)
            return True
        else:
            return False

