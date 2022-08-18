AUTHORS:

jshackles, Stumpokapow, Michael Noble.

********* UPDATED FOR PYTHON 3 ***************** 2021-06-25

********* UPDATED FOR NEW API ****************** 2022-08-18


REQUIREMENTS:

The script needs these Python packages to run:
 * requests
 * beautifulsoup4
 * pillow (with jpeg and tk support)
 * colorama

Examples for Arch:
pacman -S python-beautifulsoup4 python-requests python-pillow python-colorama tk


SETUP:
* Log in to steam on a browser
* Search your cookies for store.steampowered.com | Firefox user can use *Shift-F9 to inspect cookie data *(Firefox v98.0 tested)
* Edit setting.txt and copy-paste sessionid Content (an alpha-numerical code) from cookie data to the first field,
then copy steamLoginSecure Content (really long alpha-numerical code) from cookie into the second field in settings.txt.
* Save settings.txt and exit

** Note: Steam login session will only last ~24hrs or less and will generate a new code when you log back in. Follow the above steps to get a new code.


HOW TO RUN:
1.) open terminal and cd to idle master folder
2.) python ./start.py

SORTING:
* Edit the setting.txt and in the sort field add the following

    > mostcards     (idles game with the most card drops remaining)
    > leastcards    (idles game with the least card drops remaining)
    > mostvalue     (idles game with the most expensive card drops remaining)
    > leastvalue    (idles game with the least expensive card drops remaining)


** The old "Enhanced Steam" API was taken down but was revived by "IsThereAnyDeal" with a new
browser extention and API, the new API is called "Augmented Steam". None of the APIs use user
data but are only used to check the cards average price on steam market place and sort which
games to idle appropriately.


LICENCE:
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. A copy of the GNU General Public License can be found at 
http://www.gnu.org/licenses/. For your convenience, a copy of this license is included.