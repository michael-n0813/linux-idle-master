## UPDATES

### UPDATED v2.1 - USER MENU :: 2023-10-13

VERSION 2.1 UPDATE
 * More code cleanup
 * Fixed game name function
 * Added user menu options for idling games (Press `Ctrl-C` to access menu while idling games)
 	* q - Quit
 	* r - Resume idling
 	* s - Skip game (will skip idling this game)
 	* b - Blacklist game (add appID to blacklist.txt)

## REQUIREMENTS

The script needs these Python packages to run:
 * requests
 * beautifulsoup4
 * pillow (with jpeg and tk support)
 * colorama

Example for Arch:
`pacman -S python-beautifulsoup4 python-requests python-pillow python-colorama tk`

## SETUP
1. Log in to steam on a browser
2. Search your cookies for store.steampowered.com (Firefox user can use Shift-F9 to inspect cookie data _Firefox v98.0 tested_)
3. Copy settings-template.txt and rename to settings.txt
4. Edit setting.txt and copy-paste sessionid Content (an alpha-numerical code) from cookie data to the first field
5. Copy steamLoginSecure Content (really long alpha-numerical code) from cookie into the second field in settings.txt
6. Save settings.txt and exit

>[!NOTE]
>Steam login session will only last ~24hrs or less and will generate a new code when you log back in. Follow the above steps to get a new code.

### _(optional)_ BLACKLISTING GAMES
1. Create a file called blacklist.txt in the same folder as the script
2. Add game ID, each game ID should be on a seperate line
3. Save blacklist.txt and exit

### _(optional)_ SORTING
Edit the setting.txt and in the sort field add the following

 * `mostcards`     (idles game with the most card drops remaining)
 * `leastcards`    (idles game with the least card drops remaining)
 * `mostvalue`     (idles game with the most expensive card drops remaining)
 * `leastvalue`    (idles game with the least expensive card drops remaining)

>[!NOTE]
>The old "Enhanced Steam" API was taken down but was revived by "IsThereAnyDeal" with a new browser extention and API, the new API is called "Augmented Steam". None of the APIs use user data but are only used to check the cards average price on steam market place and sort which games to idle appropriately.

### HOW TO RUN
1. open terminal and `cd` to idle master folder
2. `python ./start.py`

* While idling a game press `Ctrl-C` to access menu
  * q - Quit
  * r - Resume idling
  * s - Skip game (will skip idling this game)
  * b - Blacklist game (add appID to blacklist.txt)


## AUTHORS

jshackles, Stumpokapow, Michael Noble.

## UPDATE HISTORY

### UPDATED v1.1 - PYTHON 3 :: 2021-06-25

### UPDATED v1.2 - NEW API :: 2022-08-18

### UPDATED v1.3 - BUG FIXES, LANG COMPAT :: 2023-08-18

### UPDATED v2.0 - BIG UPDATE :: 2023-08-21

VERSION 2.0 UPDATE
 * Code Cleaned up and more consistant formatting
 * Improved error handling, such as network loss and checking for cookie expiration without endless looping
 * Code updated to be more compatable with languages other than english, as long as the languages uses western arabic numerals (0-9)
 * Removed old win32 and macOS code
 * Added .gitingore and removed config files from git, to make it easier to pull updates
 * Added verioning to make it easier to troubleshoot issues
 * Idle Sleep time now scales based on card count remaining, in 10 min intervals (5 cards remain = 50 mins sleep, 2 cards remain = 20 mins sleep, etc)

## LICENCE
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. A copy of the GNU General Public License can be found at 
http://www.gnu.org/licenses/. For your convenience, a copy of this license is included.