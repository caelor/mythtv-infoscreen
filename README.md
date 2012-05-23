mythtv-infoscreen
=================

Python long poll server to support MythTV recording status &amp; progress displayed in a non-interactive web page.

Introduction
------------

This is a Python based GEvent long poll web server. It has the following features:

* Provides an internal key/value state table. This can be used to signal arbitrary system changes to the client web pages
* Provides a connection into the MythTV Backend, maintaining a list of current recordings and upcoming recordings, and making these available to client web pages.
* Provides a method of serving a background image which changes every 5 minutes.
* Provides a synchronised clock from the server to allow clients to not use their local clock.
* Provides an example 320x240 page as a demonstration of what can be achieved.


Possible Uses
-------------

This code is currently in use driving USB connected Parrot DF3120 screens, running a custom Linux firmware (see https://github.com/caelor/DF3120) which turns the frame into a USB-gadget ethernet X11 Server. Google Chrome in kiosk mode is then used to display the 320x240 page on the screen, giving a pleasing alternative to MythLCDServer for recording status.


Configuration
-------------

The server runs on port 1234 as shipped. Loading `http://<host>:1234` will show a server status screen. From here, you can view aspects of the server's state.

To display the 320x240 screen, browse to `http://<host>:1234/static/320x240/index.html` (served out of the `html/320x240` directory in the source). This page accepts configuration specified in the page location, separated by commas. There are 8 parameters that can be specified:
* `notify1key`: The key in the state table to be used for the red indicator
* `notify1value`: The value to match. When the `notify1key` key in the state table matches this value, the red indicator will be shown.
* `notify2key`/`notify2value`: As for `notify1`, but for the yellow indicator
* `notify3key`/`notify3value`: As for `notify1`, but for the green indicator
* `notify4key`/`notify4value`: As for `notify1`, but for the blue indicator

For example, the following URL would specify values for the red and green indicators: `http://<host>:1234/static/320x240/index.html#notify1key=foo,notify1value=bar,notify3key=baz,notify3value=barry`


Setting State Table Values
--------------------------

The internal state table can be set and modified using HTTP calls. This means that CURL can be used within scripts to send notifications to the clients. Contrary to a true restful design, a HTTP GET can be used to modify the state. The URL is as follows: `http://<host>:1234/state/<key>/<value>`

So to set the internal state table key "baldrick" to the value "cunningPlan", you would send a HTTP request to `http://<host>:1234/state/baldrick/cunningPlan`



