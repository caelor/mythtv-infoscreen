
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

from base import BaseConnection
from gevent import Greenlet
import time
from MythTV import MythBE, FileOps, Program, BECache, BEEventConnection, MythDB
import re

class MyMythBE(MythBE):
    @FileOps._ProgramQuery('QUERY_GETALLPENDING', header_length=1, sorted=True, recstatus=Program.rsRecording)
    def getCurrentRecordings(self, pg):
        return pg

    @FileOps._ProgramQuery('QUERY_GETALLPENDING', header_length=1, sorted=True, recstatus=Program.rsTuning)
    def getTuningRecordings(self, pg):
        return pg


class MythEventListener(BECache):
    # based on BEEventMonitor in the 0.25 Python bindings
    def __init__(self, callback = None,
                 backend=None, blockshutdown=False,
                 db=None):
        # the 3rd parameter is for "events" (e.g. true).
        super(MythEventListener, self).__init__(backend, blockshutdown, True, db)
        self.callback = callback
        self.db = MythDB()

    def _neweventconn(self):
        # this is called by the Myth python bindings once the backend/db has
        # been identified
        # level is one of: 3=system only, 2=generic only, 1=both, 0=none
        return BEEventConnection(
            self.host, self.port, self.db.gethostname(),
            level=3
            )

    def _listhandlers(self):
        # this is called by the Myth python bindings, and is used to register
        # the eventMonitor method below as a handler of events
        return [ self.eventMonitor ]

    def eventMonitor(self, event=None):
        # the event handler method. It needs to return a regex to match its
        # handled events, if called without an event. Otherwise, it should
        # handle the event.
        if event is None:
            return re.compile('BACKEND_MESSAGE')

        self.callback(event)


class MythTVConnection(BaseConnection):
    def __init__(self):
        super(MythTVConnection, self).__init__()
        self.backend = MyMythBE()
        self.eventHandler = MythEventListener(self._eventCallback)
        self.recordingState = []
        self.upcomingState = []
        self.recordingChecksum = 0
        self.upcomingChecksum = 0
        self.greenlet = Greenlet.spawn(self._greenlet, self)

    def shutdown(self):
        super(MythTVConnection, self).shutdown()
        print "Killing MythTV Greenlet"
        self.greenlet.kill()

        print "Cleanly disconnecting from MythTV"
        del self.eventHandler
        del self.backend


    def _greenlet(self,actor):
        print "MythTV Greenlet running"
        keepRunning = True
        while keepRunning:
            try:
                print "(MythTV Periodic running)"
                actor.updateRecordings()
                actor.updateUpcoming()
                time.sleep(120)
            except Greenlet.GreenletExit:
                keepRunning = False
            except:
                pass
        print "MythTV Greenlet finishing."
       
    def _deferredRecordingUpdate(self, actor):
        print "Deferred recording update waiting"
        time.sleep(10)
        print "Deferred updating recordings"
        actor.updateRecordings()
        actor.updateUpcoming()
        print "Deferred greenlet done"

    def _eventCallback(self, event):
        print event
        if event.startswith('BACKEND_MESSAGE[]:[]SYSTEM_EVENT SCHEDULER_'):
            self.updateUpcoming()
      
        if event.startswith('BACKEND_MESSAGE[]:[]SYSTEM_EVENT REC_'):
            # sometimes we need to wait a second or so, for recordings to actually start.
            print "Recording backend event. Triggering deferred greenlet."
            Greenlet.spawn(self._deferredRecordingUpdate, self)
            #time.sleep(10)
            #self.updateRecordings()

            #self.updateUpcoming()   # the new recording is likely to have vanished from upcoming
      

    def _createDictFromProgram(self, prog):
        return {
          'program': {
            'title': prog.title,
            'subtitle': prog.subtitle,
            'description': prog.description,
            'season': prog.season,
            'episode': prog.episode,
            'subtitle_type': prog.subtitle_type,
            'year': prog.year
          },
          'channel': {
            'number': prog.channum,
            'callsign': prog.callsign,
            'name': prog.channame
          },
          'schedule': {
            'start': time.mktime(prog.starttime.timetuple()),
            'end': time.mktime(prog.endtime.timetuple()),
          },
          'myth': {
            'host': prog.hostname,
            'source': prog.sourceid,
            'card': prog.cardid,
            'input': prog.inputid
          }
        }

    def updateRecordings(self):
        print "Updating current recordings list"
        currentList = self.backend.getCurrentRecordings()
        newState = []
        checksum = 0
        # it would be nice to eventually group these by input group.
        for current in currentList:
            p = self._createDictFromProgram(current)
            newState.append(p)
            checksum = checksum ^ hash(p['program']['title']) ^ hash(p['program']['subtitle'])

        print "Recording checkum %s vs %s" % (self.recordingChecksum, checksum)
        if (self.recordingChecksum != checksum) or (checksum == 0):
            print "  - Sending recording update"
            self.recordingChecksum = checksum
            self.recordingState = newState
            self._notify('RECORDING')


    def updateUpcoming(self):
        upcomingList = self.backend.getUpcomingRecordings()
        newState = []
        checksum = 0
        for upcoming in upcomingList:
            p = self._createDictFromProgram(upcoming)
            newState.append(p)
            checksum = checksum ^ hash(p['program']['title']) ^ hash(p['program']['subtitle'])

        print "Upcoming checkum %s vs %s" % (self.upcomingChecksum, checksum)
        if self.upcomingChecksum != checksum:
            self.upcomingChecksum = checksum
            self.upcomingState = newState
            self._notify('SCHEDULE')

