
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

import mimetypes
from handler import RequestHandler
from gevent import queue
import os
import string
import json
import pprint

class PushMessageChannel(RequestHandler):
    def __init__(self, matchRe, messageBroker):
        super(PushMessageChannel, self).__init__(matchRe)
        self.messageBroker = messageBroker


    def getExtraParams(self, path, mo):
        channel = mo.group(1)
        return {
          'queue': self.messageBroker.getTransitoryQueue(channel)
        }

    def getHeaders(self, path, mo, environ):
        # mo should contain the path to the requested file.
        resultCode = "200 OK"
        headers = [
          ('Content-Type', 'application/json')
        ]
        return (resultCode, headers)


    def handleRequest(self, mo, body, params, environ):
        # this is called in an eventlet
        endpointIdent = mo.group(1)
        endpoint = self.messageBroker.getEndpoint(endpointIdent, False)
        body.put(' ' * 1024)
        if not(endpoint):
            print "! %s: Unregistered endpoint request." % endpointIdent
            body.put(json.dumps({ 'status': 'unregistered' }))
            body.put(StopIteration)
            return


        outputQueue = endpoint.getQueue()
        endpoint.resetTimer()
        endpoint.setWaiting(True)

        message = None
        try:
            message = outputQueue.get(block=True, timeout=60)
        except queue.Empty:
            pass

        if not(message is None):
            channelObj = self.messageBroker.getChannel(message['channel'])
            #print "  %s: Pushing message from channel %s" % (endpointIdent, message['channel'])
            res = {
                'status': 'success',
                'channel': message['channel'],
                'state': message['message']
            }
            body.put(json.dumps(res))
            if channelObj.debug:
                print pprint.pprint(res, indent=4)
        else:
            body.put(json.dumps({ 'status': 'nodata' }))

        endpoint.setWaiting(False)
        body.put(StopIteration)

        return
