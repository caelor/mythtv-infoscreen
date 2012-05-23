
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
from gevent import Greenlet

class Endpoint:
    # This class represents a single client, which can be subscribed to
    # an arbitrary number of channels.
    # It manages the connection of the client side of Registration objects
    # and converges them into a single Queue, which can be passed to
    # an appropriate client.

    # timeout period in seconds (10 minutes)
    TIMEOUT = 80.0

    # note, this timer should be larger than the poll frequency, otherwise
    # the endpoint could get cleaned up between valid polls.

    def __init__(self, broker, ident, desc):
        self.lastRequest = time.time()
        self.outputQueue = queue.Queue()
        self.registrations = {}
        self.broker = broker
        self.ident = ident
        self.desc = desc
        self.isWaiting = False

    def finish(self):
        for reg in self.registrations:
            self.registrations[reg]['registration'].unregister()

    # static method 
    def _channelHandler(self, params):
        # this runs in a greenlet, with an instance for each subscription.
        # they all contribute into a single outputQueue, which will then
        # be received by an appropriate output handler.
        actor = params['self']
        channel = params['channel']
        while channel in actor.registrations.keys() and actor.outputQueue:
            reg = actor.registrations[channel]['registration']
            message = None
            try:
                message = reg.getQueue().get(True,10)
            except queue.Empty:
                pass

            if message and actor.outputQueue:
                actor.outputQueue.put({
                  'channel': channel,
                  'message': message
                })

        # exit from the channel handler if our world falls apart.
        pass  

    def isSubscribed(self, channel):
        return channel in self.registrations.keys()


    def subscribe(self, channel):
        channelObj = self.broker.getChannel(channel)
        if not(channelObj):
            return None

        registration = channelObj.getRegistration(self.ident)
        self.registrations[channel] = {
          'registration': registration
        }

        self.registrations[channel]['greenlet'] = Greenlet.spawn(
            self._channelHandler, 
            { 'self': self, 'channel': channel }
            )
        return channelObj.getState()

    def unsubscribe(self, channel):
        if (channel in self.registrations.keys()):
            # this will also cause the greenlet to stop
            self.registrations[channel].unregister()


    def isStale(self):
        now = time.time()
        return (now - self.lastRequest) > Endpoint.TIMEOUT

    def getQueue(self):
        return self.outputQueue

    def resetTimer(self):
        self.lastRequest = time.time()

    def getAge(self):
        return time.time() - self.lastRequest

    def getDescription(self):
        return self.desc

    def getSubscriptions(self):
        return self.registrations.keys()

    def getQueueSize(self):
        return self.outputQueue.qsize()

    def getWaiting(self):
        return self.isWaiting

    def setWaiting(self, state):
        self.isWaiting = state
