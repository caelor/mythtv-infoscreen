
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

import mimetypes
from handler import RequestHandler
import os
import string
import time
import random

class RandomImageHandler(RequestHandler):
    UPDATE_FREQUENCY=300

    def __init__(self, matchRe, imgDir, fallbackDir):
        super(RandomImageHandler, self).__init__(matchRe)

        self.imgDir = imgDir
        self.fallbackDir = fallbackDir
        mimetypes.init()

        self.currentImage = None

        self.greenlet = Greenlet.spawn(self._imageRotator, self)


    def _imageRotator(self, actor):
        while True:
            options = os.listdir(actor.imgDir)
            dirUsed = actor.imgDir
            if len(options) < 1:
                options = os.listdir(actor.fallbackDir)
                dirUsed = actor.fallbackDir

            ref = random.randint(0, len(options) - 1)
            actor.currentImage = os.path.join(dirUsed, options[ref])

            print "Current random image is %s" % actor.currentImage
            
            time.sleep(RandomImageHandler.UPDATE_FREQUENCY)


    def getHeaders(self, path, mo, environ):
        # mo should contain the path to the requested file.
        resultCode = "404 NOT FOUND"
        headers = [
          ('Content-Type', 'text/html')
        ] 

        if self.currentImage:
            (mimeType, encoding) = mimetypes.guess_type(self.currentImage)
            if not(mimeType):
                mimeType = 'text/plain'

            resultCode = "200 OK"
            headers = [
              ('Content-Type', mimeType)
            ]

        return (resultCode, headers)


    def handleRequest(self, mo, body, params, environ):

        if not(self.currentImage):
            body.put('<html><body>')
            body.put('<h1>404 Not Found</h1>')
            body.put('<p>This resource is temporarily unavailable.<p>')
            body.put('</body></html>')
            body.put(StopIteration)
        else:
            fh = open(self.currentImage, 'rb')
            body.put(fh.read())
            body.put(StopIteration)
            fh.close()

        return
