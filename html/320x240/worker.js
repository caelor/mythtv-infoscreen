
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

/* *** Global Subscriptions *** */

// perform channel subscriptions
$(document).bind('mythScreen-Ready', function() {
  mythScreen.subscribeChannel('periodic.time');
  mythScreen.subscribeChannel('state.misc');
  mythScreen.subscribeChannel('state.mythbackend.upcoming');
  mythScreen.subscribeChannel('state.mythbackend.current');

  $('#currentlyRecordingScreen').hide();
  $('#timeUntilNextRecording').hide();
  $('#idleScreen').show();
});


// general debugging logging
$(document).bind('mythScreen-Update', function(e, params) {
  console.log("Channel updated: " + params.channel);
});




/* *** Background Image Handling *** */
$(document).bind('mythScreen-Ready', function(e, params) {
  $('#imageBackground').html('');
  $('<img></img>').attr('src', '../../image/random').appendTo($('#imageBackground'));
});
$(document).bind('mythScreen-Update', function(e, params) {
  if (params.channel == 'periodic.time') {
    var t = params.state.match(/\d{4}-\d{2}-\d{2} \d{2}:(\d{2}).*/)
    if (t[1] == '00' || t[1] == '15' || t[1] == '30' || t[1] == '45') {
      $('#imageBackground img').attr('src', '../../image/random?' + new Date());
    }
  }
});


/* *** Update clocks *** */
$(document).bind('mythScreen-Update', function(e, params) {
  if (params.channel == 'periodic.time') {
    var t = params.state.match(/(\d{2}:\d{2} \w{2})$/);
    $('#bigClock').text(t[1]);
    $('#littleClock').text(t[1]);
  }
});


/* *** Update notification bars *** */
$(document).bind('mythScreen-Update', function(e, params) {
  if ((params.channel == 'state.misc') && params.state){
    // it's a state table update.
    for (var i=0; i<5; i++) {
      var el = $('#indicator' + i);
      var el2 = $('#littleindicator' + i);
      var configItemKey = 'notify' + i + 'key';
      var configItemValue = 'notify' + i + 'value';
      if ((configItemKey in config) && (configItemValue in config)) {
        var onMatchState = config[configItemKey];
        var onMatchValue = config[configItemValue];
        if (onMatchState in params.state) {
          if (params.state[onMatchState] == onMatchValue) {
            el.addClass('active');
            el2.addClass('active');
          }
          else {
            el.removeClass('active');
            el2.removeClass('active');
          }
        }
        else {
          el.removeClass('active');
          el2.removeClass('active');
        }
      }
      else {
        el.removeClass('active');
        el2.removeClass('active');
      }
    } 
  }
});


/* *** Recording soon notice *** */
$(document).bind('mythScreen-Update', function(e, params) {
  if ((params.channel == 'periodic.time') && ('state.mythbackend.upcoming' in mythScreen.state)) {
    if (mythScreen.state['state.mythbackend.upcoming']) {
      // we have at least 1 upcoming recording.
      // figure out how long until the next recording.
      var nextRecording = mythScreen.state['state.mythbackend.upcoming'][0];
      var now = (new Date()) / 1000;
      var delta = nextRecording.schedule.start - now;
      var minutes = Math.floor(delta / 60); 
      // set an upper bound of 90 minutes
      console.log(minutes + ' minutes until next recording');
      if (minutes < 2) {
        $('#timeUntilNextRecording').show().text('Recording about to start');
      }
      else if (minutes <= 30) {
        $('#timeUntilNextRecording').show().text('Next recording in ' + minutes + ' mins');
      }
      else {
        $('#timeUntilNextRecording').hide();
      }
    }
    else {
      $('#timeUntilNextRecording').hide();
    }
  }
});



/* *** Current Recordings List *** */
$(document).bind('mythScreen-Update', function(e, params) {
  if (params.channel == 'state.mythbackend.current') {
    // delete any pre-existing recording notices
    $('#recordings').html('');
    console.log('reset recordings');

    $.each(params.state.list, function(k,v) {
      // construct a recording object to append
      var recDiv = $('<div></div>').addClass('recProgress');
      recDiv.attr('start', v.schedule.start);
      recDiv.attr('end', v.schedule.end);
      $('<div></div>').addClass('progressBar').appendTo(recDiv);
      var marqueeText = $('<span></span>').addClass('marquee').appendTo(recDiv);
      var t = v.program.title;
      if (v.program.subtitle) {
        t = t + ' - ' + v.program.subtitle;
      }
      //marqueeText.text(t);
      var marqueeInner = $('<span></span>').appendTo(marqueeText).text(t);
      /*$('<span></span>').addClass('channel').text(v.channel.callsign).appendTo(marqueeText);
      $('<span></span>').addClass('title').text(v.program.title).appendTo(marqueeText);
      if (v.program.subtitle) {
        $('<span></span>').addClass('subtitle').text(' - ' + v.program.subtitle).appendTo(marqueeText);
      }*/

      recDiv.appendTo($('#recordings'));

      marqueeInner.attr('scrollamount', 2);
      marqueeInner.attr('width', marqueeText.width());
      marqueeInner.attr('height', marqueeText.height());
      marqueeInner.marquee();
    });

    doProgressUpdate();

    if (params.state.list) {
      if (params.state.list.length > 0) {
        $('#currentlyRecordingScreen').show();
        $('#idleScreen').hide();
      }
      else {
        $('#currentlyRecordingScreen').hide();
        $('#idleScreen').show();
      }
    }
    else {
      $('#currentlyRecordingScreen').hide();
      $('#idleScreen').show();
    }
  }
});


setTimeout(progressUpdater, 1000);
function progressUpdater() {
  doProgressUpdate();
  setTimeout(progressUpdater, 10000); // every 10 seconds
}

function doProgressUpdate() {
  $.each($('#recordings .recProgress'), function(k,v) {
    var start = $(v).attr('start');
    var end = $(v).attr('end');
    var now = (new Date()) / 1000;
    var l = end-start;
    var d = now-start;
    var pct = (d * 100) / l;
    $(v).children('.progressBar').width(pct + '%');

    if (now > end) {
      var delta = now - end;
      // every 30 seconds after a program overruns, poke the server for an update to recording state.
      if (now%30 == 0) {
        console.log('Program has overrun. Requesting update from server.');
        mythScreen.subscribeChannel('state.mythbackend.current');
      }
    }
  });
}
