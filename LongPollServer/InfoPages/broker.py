
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

import string

class BrokerInfoPage:
    def __init__(self, broker):
        self.broker = broker

    def getExtraParams(self, path, mo):
        return self.broker

    def handleRequest(self, mo, body, extra):
        body.put('<html><body>')
        body.put('<h1>Message Broker status</h1>')

        body.put('<h2>Channels</h2>')
        body.put('<ul>')
        for channel in self.broker.getChannels():
            details = self.broker.getChannelDetails(channel)
            body.put('<li>')
            body.put('%s (%d registrations, %d total messages sent)' % (
                channel, details['registrations'], details['messages'])
                )
            body.put(' (<a href="/refresh/%s">Force Refresh</a>)' % channel)
            body.put(' (Debugging <a href="/debug/channel/%s/1">Enable</a>' % channel)
            body.put(' | <a href="/debug/channel/%s/0">Disable</a>)' % channel)
            body.put('</li>')
        body.put('</ul>')

        body.put('<h2>Endpoints</h2>')
        body.put('<ul>')
        for endpoint in self.broker.getEndpoints():
            details = self.broker.getEndpointDetails(endpoint)
            body.put('<li>%s [%s] (%d messages outstanding, %s seconds since last request, client connected: %s, subscribed to: %s)</li>' % (
                endpoint, 
                details['desc'], 
                details['queueSize'], 
                details['age'],
                details['isWaiting'],
                string.join(details['subscriptions'], ', '))
            )
        body.put('</ul>')

        body.put('</body></html>')
        body.put(StopIteration)
        pass

