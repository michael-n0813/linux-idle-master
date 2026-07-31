## ABOUT

**Linux Idle Master** is a simple CLI Script to idle steam games for card drops  
>Only linux based operating systems are supported

## UPDATES
### UPDATED v3.1 - WHITELIST :: 2026-08-01

VERSION 3.1 UPDATE
 * Added whitelist support
 * Added whitelist to options menu

>[!IMPORTANT]
>Version 3.0 has changed a lot, I recommend a fresh clone of the respository to avoid any issues or confussion.

## INSTALLING

**OPTION A** (requires `git` package)  
From a terminal enter  
`git clone https://github.com/michael-n0813/linux-idle-master.git`

**OPTION B**  
Download a zip file from releases and extract the folder  
https://github.com/michael-n0813/linux-idle-master/releases

## REQUIREMENTS

The script needs these Python packages to run:
 * requests
 * beautifulsoup4
 * pillow (with jpeg and tk support)

Example for Arch:  
`pacman -S python-beautifulsoup4 python-requests python-pillow tk`

## HOW TO RUN
 1. Open a terminal and `cd` to idle master folder
 1. Enter `python ./start.py`

 * While idling a game press `Ctrl-C` to access menu
    * q - Quit
    * r - Resume idling
    * s - Skip game *(will skip idling this game)*
    * b - Blacklist game *(add appID to blacklist.txt)*
    * w - Whitelist game *(add appID to whitelist.txt)*

## SETUP
>For first time setup, run the script once to generate settings.conf file
 1. Log in to https://steamcommunity.com/ on a web browser of your choice
 1. Search your cookies for steamcommunity.com *(Firefox user can use Shift-F9 to inspect cookie data)*
 1. Edit settings.conf and copy-paste 'sessionid' content *(an alpha-numerical code)* from cookie data to the first field
 1. Copy-paste 'steamLoginSecure' content *(really long alpha-numerical code)* from cookie data into the second field

>[!IMPORTANT]
>store.steampowered.com and steamcommunity.com use different cookie data, if you get the error `Invalid cookie data, cannot log into Steam` then make sure you are using the cookie data from steamcommunity.com and **NOT** store.steampowered.com.

>[!NOTE]
>Steam login session will only last ~24hrs or less and will generate a new code when you log back in. Follow the above steps to get a new code.

### *(optional)* STEAMPARENTAL

>[!NOTE]
>Unless you **need** this feature it can ignored and left as default `""`

This is only used if using steam parental conrols  

 1. Log in to https://steamcommunity.com/ on a web browser of your choice
 1. Search your cookies for steamcommunity.com *(Firefox user can use Shift-F9 to inspect cookie data)*
 1. Edit the settings.conf file and copy-paste 'steamParental' content from cookie data to the third field

### *(optional)* SORTING

Edit the settings.conf file and in the 'sort' field add the following  

 * `""`            *(Default, no sorting)*  
 * `mostcards`     *(idles game with the most card drops remaining)*  
 * `leastcards`    *(idles game with the least card drops remaining)*

### *(optional)* HASPLAYTIME

Edit the settings.conf file and in the 'hasPlaytime' field set `true` or `false` *(default `false`)*  

>When set to true, only games that have been launched previously will be idled, games that are unplayed and have no playtime will not.

### *(optional)* BLACKLISTING GAMES

 1. Create a file called blacklist.txt in the same folder as the script
 1. Add game ID, each game ID should be on a seperate line
 1. Save blacklist.txt and exit

>When blacklisting games from the options menu, a blacklist.txt file will be created automatically if the file does not exist.

### *(optional)* WHITELISTING GAMES

 1. Create a file called whitelist.txt in the same folder as the script
 1. Add game ID, each game ID should be on a seperate line
 1. Save whitelist.txt and exit

>When whitelisting games from the options menu, a whitelist.txt file will be created automatically if the file does not exist.

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
 * Added versioning to make it easier to troubleshoot issues
 * Idle Sleep time now scales based on card count remaining, in 10 min intervals (5 cards remain = 50 mins sleep, 2 cards remain = 20 mins sleep, etc)

### UPDATED v2.1 - USER MENU :: 2023-10-13

VERSION 2.1 UPDATE
 * More code cleanup
 * Fixed game name function
 * Added user menu options for idling games (Press `Ctrl-C` to access menu while idling games)
    * q - Quit
    * r - Resume idling
    * s - Skip game (will skip idling this game)
    * b - Blacklist game (add appID to blacklist.txt)

### UPDATED v2.2 - COOKIES, PATH CHECKING, ERROR :: 2024-05-09

VERSION 2.2 UPDATE
 * Added cookie setting to fix idle count for non-English users
 * Added Python3 Path checking
 * Fixed SyntaxWarning

### UPDATED v3.0 - BIG UPDATE :: 2025-10-20

VERSION 3.0 UPDATE
 * Replaced settings.txt with settings.conf
 * Added feature to create settings.conf if file not found
 * Removed settings-template.txt from repository
 * Lots of bug fixes, error handling improvments
 * Reduced API calls for getting app name
 * Improved logging with error levels and clean output
 * Log file now appends output, not overwritten
 * Removed API dependant sorting options (mostvale, leastvalue)
 * Removed python-colorama dependency requirement
 * Implemented releases for easier version control

## LICENCE
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. A copy of the GNU General Public License can be found at 
http://www.gnu.org/licenses/. For your convenience, a copy of this license is included.