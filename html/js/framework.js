
/*

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


 */
if (typeof jQuery == 'undefined') {
  alert('The framework requires jQuery to be loaded (try /static/js/jquery.min.js)');
}

var mythScreen = {
  uuid: null,
  isInit: false,
  initInProcess: false,
  state: {},
  oldState: {},

  init: function() {
    if (!mythScreen.initInProcess && !mythScreen.isInit) {
      mythScreen.initInProcess = true;
      mythScreen.ident = 'WebClient';
      if (typeof IDENTIFIER != 'undefined') {
        mythScreen.ident = encodeURIComponent(IDENTIFIER);
      }
      $.ajax({
        type: 'POST', 
        async: true,
        cache: false,
        timeout: 5000,
        url: '/channel/register/' + mythScreen.ident,
        success: mythScreen.registerResponse,
        error: mythScreen.registerError,
        dataType: 'json'
      });
    }
  },

  registerError: function(jqXHR, textStatus, errorThrown) {
    alert('Error initializing framework: ' + textStatus + ', ' + errorThrown);
  },

  registerResponse: function(data) {
    if (data.status == 'success') {
      mythScreen.uuid = data.uuid
      mythScreen.isInit = true;
      mythScreen.initInProcess = false;
      $(document).trigger('mythScreen-Ready')
      mythScreen.poll();
    }
  },

  poll: function() {
    console.log('Poll start');
    if (mythScreen.isInit) {
      $.ajax({
        type: 'GET', 
        async: true,
        cache: false,
        timeout: 120000,
        url: '/channel/longpoll/' + mythScreen.uuid,
        success: mythScreen.pollSuccess,
        error: mythScreen.pollError,
        dataType: 'json'
      });
    }
  },

  pollSuccess: function(data) {
    if (data.status == 'success') {
      if (data.channel in mythScreen.state) {
        mythScreen.oldState[data.channel] = mythScreen.state[data.channel];
      }
      mythScreen.state[data.channel] = data.state;
      console.log('[' + data.channel + '] ' + data.state);

      $(document).trigger('mythScreen-Update', { 'channel': data.channel, 'state': data.state })
      mythScreen.poll();
    }
    else {
      if (data.status == 'unregistered') {
        mythScreen.isInit = false;
        mythScreen.init();
      }
      else {
        setTimeout(mythScreen.poll, 2000); // continue in 2 seconds
      }
    }
  },

  pollError: function(jqXHR, textStatus, errorThrown) {
    $(document).trigger('mythScreen-PollError', { 'status': textStatus, 'error': errorThrown })
    console.log('Error polling. Deferring 2 seconds');
    setTimeout(mythScreen.poll, 2000); // continue in 2 seconds
  },

  subscribeChannel: function(channel) {
    if (!mythScreen.isInit) { 
      alert('Unable to subscribe to channel - framework is not ready');
      return false;
    }

    $.ajax({
      type: 'POST',
      async: true,
      cache: false,
      timeout: 5000,
      url: '/channel/subscribe/' + channel + '/' + encodeURIComponent(mythScreen.uuid),
      success: mythScreen.subscribeSuccess
    });
  },

  subscribeSuccess: function(data) {
    if (data.status == 'success') {
      mythScreen.state[data.channel] = data.state;
      $(document).trigger('mythScreen-Update', { 'channel': data.channel, 'state': data.state })
    }
  }

};

$(document).bind('ready', function() {
  // init the framework
  if (!mythScreen.isInit) {
    mythScreen.init();
  }
});
