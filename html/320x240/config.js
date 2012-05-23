
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


/* *** Parse Configuration *** */

// parse the window.location.hash into a config
function parseConfig() {
  var foo = window.location.hash.slice(1).split(',');
  var res = {};
  $.each(foo, function(k, v) {
    v2 = v.split('=');
    if (v2[0]) {
      res[v2[0]] = v2[1];
      console.log('Config: ' + v2[0] + '=' + v2[1]);
    }
  });

  return res;
}
var config = parseConfig();



