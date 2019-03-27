AUTHORS:

jshackles, Stumpokapow, Michael Noble.


REQUIREMENTS:

The script needs these Python 2 packages to run:
requests
beautifulsoup4
pillow (with jpeg and tk support)
colorama

Examples for packages that meet the dependencies:
Ubuntu: python-bs4, python-requests, python-pil.imagetk, python-colorama
Arch Linux: python2-beautifulsoup4, python2-requests, python2-pillow, tk, python2-colorama


SETUP:
* Log in to steam on a browser
* Search your cookies for store.steampowered.com
* Edit setting.txt and copy-paste sessionid Content (an alpha-numerical code) from cookie data to the first field,
then copy steamLoginSecure Content (really long alpha-numerical code) from cookie into the second field in settings.txt.
* Save settings.txt and exit

**Note: Steam login session will only last ~24hrs or less and will generate a new code when you log back in. Follow the above steps to get a new code.


HOW TO RUN:
open terminal and cd to idle master folder
type:
    python2 ./start.py


LICENCE:
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. A copy of the GNU General Public License can be found at 
http://www.gnu.org/licenses/. For your convenience, a copy of this license is included.
