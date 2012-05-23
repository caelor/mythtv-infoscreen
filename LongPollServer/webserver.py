
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

from gevent import monkey
monkey.patch_thread()
monkey.patch_time()

from gevent import pywsgi
from gevent import Greenlet
from gevent import queue
import time

class WebServer:
    def __init__(self, host, port, handlers):
        self.host = host
        self.port = port
        self.handlers = handlers

        self.server = pywsgi.WSGIServer(
            (self.host, self.port), 
            self.handle_request,
            log=None
            )
        print "Starting server..."
        self.server.start()


    def __del__(self):
        self.server.stop()


    def runHandler(self, params):
        body = params['body']
        handler = params['handler']
        mo = params['mo']
        extra = params['extra']
        environment = params['environment']

        handler.handleRequest(mo, body, extra, environment)
        body.put(StopIteration)


    def notFoundError(self, body):
        body.put('''<html><body>
               <h1>404 Error</h1>
               <p>The page you requested does not exist. Please check your details and try again.</p>
             </body></html>''')
        body.put(StopIteration)
        

    def handle_request(self,environ, start_response):
        path = environ['PATH_INFO']
        selectedHandler = None
        for handler in self.handlers:
            mo = handler.getMatchRegex().match(path)
            if mo:
                selectedHandler = {
                  'handler': handler,
                  'mo': mo,
                }

        body = queue.Queue()
        #body.put(' ' * 1000)

        if selectedHandler:
            extraParams = None
            try:
                extraParams = selectedHandler['handler'].getExtraParams(path, selectedHandler['mo'])
            except AttributeError:
                pass

            (part1, part2) = selectedHandler['handler'].getHeaders(path, selectedHandler['mo'], environ)
            start_response(part1, part2)
            
            g = Greenlet.spawn(self.runHandler, {
              'body': body,
              'handler': selectedHandler['handler'],
              'mo': selectedHandler['mo'],
              'extra': extraParams,
              'environment': environ
            })
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            g = Greenlet.spawn(self.notFoundError, body)

        return body
