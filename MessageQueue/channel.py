
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

from gevent import queue
from gevent import Greenlet
from registration import Registration

class Channel:
    # This class represents a single channel - an identifier to which a message
    # can be published, and any number of clients can be subscribed.
    # This one->many->one relationship is achieved by using Registration objects
    # to track how many subscribers a channel has, and to pass a copy of the
    # message to each subscriber.

    def __init__(self, channelName):
        self.queue = queue.Queue()
        self.registrations = {}
        self.messageCount = 0
        self.lastMessage = ''
        self.name = channelName
        self.debug = False

        self.greenlet = Greenlet.spawn(self._messageSwitch, self)

    def __del__(self):
        del self.queue
        for f in self.registrations.keys:
            del self.registrations[f]
        

    def _messageSwitch(self, actor):
        # self will be the greenlet object
        while actor.queue:
           message = None
           try:
               message = actor.queue.get(True,10)
           except queue.Empty:
               pass

           for ident in actor.registrations.keys():
               reg = actor.registrations[ident]
               if (reg.isStale()):
                   print "Channel: Removing stale registration"
                   del actor.registrations[ident]
               elif message:
                   if actor.debug:
                       print "Bridge: %s -> %s" % (actor.name, ident)
                   actor.registrations[ident].getQueue().put(message)


    def publish(self, message):
        if self.debug:
            print "-> %s: %s" % (self.name, message)
        self.queue.put(message)
        self.lastMessage = message
        self.messageCount = self.messageCount + 1

    def getQueue(self):
        return self.queue

    def getRegistration(self, ident):
        if not(ident in self.registrations.keys()):
            self.registrations[ident] = Registration()

        return self.registrations[ident]

    def getRegistrationCount(self):
        return len(self.registrations.keys())

    def getMessageCount(self):
        return self.messageCount

    def getState(self):
        return self.lastMessage

    def forceUpdate(self):
        self.publish(self.getState())

    def setDebug(self, state):
        self.debug = state
        print "%s: Debugging set to %s" % (self.name, self.debug)
