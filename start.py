#!/usr/bin/env python
import requests
import http.cookiejar
import bs4
import time
import re
import subprocess
import sys
import os
import json
import logging
import datetime
import ctypes

# Colors
colorGreen = "\033[32m"
colorRed = "\033[31m"
colorCyan = "\033[36m"
colorYellow = "\033[33m"
colorReset = "\033[39m"

# Version
version = "v3.1"

# Directory
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Log formatting
class log_text_clean(logging.Formatter):
    def format(self, text):
        logText = super().format(text)
        cleanText = re.sub(r"\033\[\d+m", "", logText)
        return cleanText

logFormat = logging.Formatter("[%(asctime)s] %(message)s", "%d %b %Y %I:%M:%S %p")
logFileFormat = log_text_clean("[%(asctime)s][%(levelname)s][%(lineno)d] %(message)s", "%d %b %Y %I:%M:%S %p")

# File logging
logFile = logging.FileHandler("idlemaster.log", mode="a")
logFile.setFormatter(logFileFormat)
logging.basicConfig( level = logging.DEBUG, handlers = [logFile])

# Console logging
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logFormat)
logger.addHandler(console)

logger.info(colorGreen + "WELCOME TO IDLE MASTER - " + colorYellow + version + colorReset)

# Check for python 3
pyLink = "python"
try:
    subprocess.call(["python3", "--version"], stdout = subprocess.DEVNULL)
except:
    logger.error(colorRed + "Python3 not installed" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

try:
    pyOut = subprocess.check_output(["python", "--version"])
    pyVer = re.search("Python 3", str(pyOut))

    if not pyVer:
        pyLink = "python3"
        logger.warning(colorYellow + "Python pointing to incorrect version, using Python3 instead" + colorReset)
except:
    pyLink = "python3"
    logger.warning(colorYellow + "Python link incorrect, using Python3 instead" + colorReset)

# Settings.conf
authData = {}
try:
    with open("settings.conf", "r") as f:
        logger.info("Settings.conf file found, reading data...")
        for line in f:
            cleanLine = re.sub(r"[\"\n]", "", line)
            if cleanLine and not cleanLine.startswith("#"):
                key, value = cleanLine.split(" = ")
                authData[key] = value
except FileNotFoundError:
    logger.warning(colorYellow + "Settings.conf file is missing, creating file..." + colorReset)
    try:
        with open("settings.conf", "w") as f:
            f.write("# Ilde Master config file\n")
            f.write("# Open web browser and log in to https://steamcommunity.com/ to get cookie data\n\n")
            f.write("# sessionID - found in steam cookie data\n")
            f.write("sessionID = \"\"\n\n")
            f.write("# steamLoginSecure - found in steam cookie data\n")
            f.write("steamLoginSecure = \"\"\n\n")
            f.write("# steamParental - found in steam cookie data\n# !! Not needed unless using parental controls, otherwise leave blank !!\n")
            f.write("steamParental = \"\"\n\n")
            f.write("# (optional) sorting options: (\"\", mostcards, leastcards)\n")
            f.write("sort = \"\"\n\n")
            f.write("# hasPlaytime options: (true, false). If enabled(true) will only idle games previously played and not unplayed games\n")
            f.write("hasPlaytime = \"false\"")
    except:
        logger.error(colorRed + "Unable to generate settings.conf file" + colorReset)
        input("Press Enter to continue...")
        sys.exit()
    else:
        logger.info(colorGreen + "Settings.conf file successfully created" + colorReset)
        input("Press Enter to continue...")
        sys.exit()
except SystemExit:
    sys.exit()
except:
    logger.error(colorRed + "Unable to read settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

# Validate settings.conf data
for key in ["sessionID", "steamLoginSecure", "steamParental", "sort", "hasPlaytime"]:
    if not key in authData:
        logger.error(colorRed + "\"" + key + "\" missing in settings.conf file" + colorReset)
        input("Press Enter to continue...")
        sys.exit()

if authData["sessionID"] == "":
    logger.error(colorRed + "Missing \"sessionID\" value in settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

if authData["steamLoginSecure"] == "":
    logger.error(colorRed + "Missing \"steamLoginSecure\" value in settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

if not authData["sort"] in ["", "mostcards", "leastcards"]:
    logger.error(colorRed + "Invalid option for \"sort\" in settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

if not authData["hasPlaytime"].lower() in ["true", "false"]:
    logger.error(colorRed + "Invalid option for \"hasPlaytime\" in settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

myProfileURL = "https://steamcommunity.com/profiles/" + authData["steamLoginSecure"][:17]

# Generate cookies
def generate_cookies():
    global authData
    try:
        cookies = dict(sessionid = authData["sessionID"], steamLoginSecure = authData["steamLoginSecure"], steamparental = authData["steamParental"], Steam_Language = "english")
    except:
        logger.error(colorRed + "Unable to set cookies" + colorReset)
        input("Press Enter to continue...")
        sys.exit()
    return cookies

# Start idling game
def idle_open(appID, appName):
    try:
        logger.info("Starting game " + appName + " to idle cards")
        global processIdle
        global idleTime

        idleTime = time.time()
        processIdle = subprocess.Popen([pyLink, "steam-idle.py", str(appID)])
    except:
        logger.error(colorRed + "Can not launch " + appName + colorGreen + " [ AppID " + str(appID) + " ]" + colorReset)
        input("Press Enter to continue...")
        sys.exit()

# Stop idling game
def idle_close(appID, appName):
    try:
        logger.info("Closing game " + appName)
        processIdle.terminate()
        totalTime = int(time.time() - idleTime)
        logger.info(appName + " idled for " + colorGreen + str(datetime.timedelta(seconds = totalTime)) + colorReset)
    except:
        logger.error(colorRed + "Could not close game" + colorReset)
        input("Press Enter to continue...")
        sys.exit()

# Network issue idle
def chill_out(appID, appName):
    if processIdle.poll() is None:
        logger.warning(colorYellow + "Suspending operation for " + appName + colorReset)
        idle_close(appID, appName)
    stillDown = True
    while stillDown:
        try:
            logger.info("Sleeping for 5 minutes...")
            time.sleep(300)
            try:
                # Check if cookies still valid or steam is down (network issue)
                steamUp = requests.get("https://store.steampowered.com")
                rCode = steamUp.status_code
                if rCode == 200:
                    expired = cookie_test()
                    if expired:
                        idle_close(appID, appName)
                        logger.warning(colorYellow + "Cookie session expired" + colorReset)
                        input("Press Enter to continue...")
                        sys.exit()
                    else:
                        stillDown = False
                else:
                    logger.warning(colorYellow + "Still unable to connect to Steam" + colorReset)
            except SystemExit:
                sys.exit()
            except:
                logger.warning(colorYellow + "Still unable to find drop info" + colorReset)
        except:
            logger.error(colorRed + "Unknown network issue" + colorReset)
            input("Press Enter to continue...")
            sys.exit()
    logger.info(colorGreen + "Connection established, resuming idling" + colorReset)

# Get app name
def get_app_name(appID):
    try:
        api = requests.get("https://store.steampowered.com/api/appdetails/?appids=" + str(appID) + "&filters=basic")
        apiData = json.loads(api.text)
        return colorCyan + apiData[str(appID)]["data"]["name"] + colorReset
    except:
        logger.warning(colorYellow + "Unable to get app name" + colorReset)
        return colorCyan + "App " + str(appID) + colorReset

# Get blacklist
def get_blacklist():
    try:
        with open("blacklist.txt", "r") as f:
            lines = f.readlines()
        blacklist = [int(n.strip()) for n in lines]
    except:
        blacklist = [];

    if not blacklist:
        logger.info("No games have been blacklisted")

    return blacklist

# Get whitelist
def get_whitelist():
    try:
        with open("whitelist.txt", "r") as f:
            lines = f.readlines()
        whitelist = [int(n.strip()) for n in lines]
    except:
        whitelist = [];

    if not whitelist:
        logger.info("No games have been whitelisted")

    return whitelist

# Add game to blacklist
def blacklist_game(appID):
    try:
        with open("blacklist.txt", "a") as f:
            f.write(str(appID) + "\n")
    except:
        logger.error(colorRed + "Failed to blacklist game" + colorReset)

# Add game to whitelist
def whitelist_game(appID):
    try:
        with open("whitelist.txt", "a") as f:
            f.write(str(appID) + "\n")
    except:
        logger.error(colorRed + "Failed to whitelist game" + colorReset)

# Check if cookies valid
def cookie_test():
    try:
        r = requests.get(myProfileURL + "/badges/", cookies = cookies)
        badgePageData = bs4.BeautifulSoup(r.text, "html.parser")
        userinfo = badgePageData.find("a", {"class": "user_avatar"})
        if userinfo:
            return False
        else:
            return True
    except:
        return True

# Get card drops
logger.info("Finding games that have card drops remaining...")
try:
    cookies = generate_cookies()
    r = requests.get(myProfileURL + "/badges/", cookies = cookies)
except SystemExit:
    sys.exit()
except:
    logger.error(colorRed + "Unable to read badge page" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

try:
    badgesLeft = []
    badgePageData = bs4.BeautifulSoup(r.text, "html.parser")
    badgeSet = badgePageData.find_all("div", {"class": "badge_title_stats"})
except:
    logger.error(colorRed + "Could not find drop info" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

# For profiles with multiple pages
try:
    badgePages = int(badgePageData.find_all("a", {"class": "pagelink"})[-1].text)
    if badgePages:
        logger.info(str(badgePages) + " badge pages found, gathering additional data...")
        currentpage = 2
        while currentpage <= badgePages:
            r = requests.get(myProfileURL + "/badges/?p=" + str(currentpage), cookies = cookies)
            badgePageData = bs4.BeautifulSoup(r.text, "html.parser")
            badgeSet = badgeSet + badgePageData.find_all("div", {"class": "badge_title_stats"})
            currentpage = currentpage + 1
except:
    logger.info("Reading badge page, please wait...")

# User badge page error checking
if not badgePageData.find("a", {"class": "user_avatar"}):
    logger.error(colorRed + "Invalid cookie data, cannot log in to Steam" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

# Gather list of games to idle
blacklist = get_blacklist()
whitelist = get_whitelist()
whitelistOnly = False

if whitelist:
    logger.warning(colorYellow + "Whitelisted games found, idling only whitelisted games" + colorReset)
    whitelistOnly = True

for badge in badgeSet:
    try:
        badgeText = badge.get_text()
        dropCount = badge.find_all("span", {"class": "progress_info_bold"})[0].contents[0]
        Playtime = re.search("hrs on record", badgeText) != None

        if "No card drops" in dropCount or (Playtime == False and authData["hasPlaytime"].lower() == "true"):
            continue
        else:
            # Remaining drops
            dropCountInt, junk = dropCount.split(" ", 1)
            dropCountInt = int(dropCountInt)
            linkGuess = badge.find_parent().find_parent().find_parent().find_all("a")[0]["href"]
            junk, badgeID = linkGuess.split("/gamecards/", 1)
            badgeID = int(badgeID.replace("/", ""))
            if whitelistOnly:
                if badgeID in whitelist:
                    push = [badgeID, dropCountInt, 0]
                    badgesLeft.append(push)
            else:
                if badgeID in blacklist:
                    logger.warning(colorCyan + "App " + str(badgeID) + colorYellow + " on blacklist, skipping game..." + colorReset)
                    continue
                else:
                    push = [badgeID, dropCountInt, 0]
                    badgesLeft.append(push)
    except:
        continue

# Sort list of games to idle
if authData["sort"] == "":
    games = badgesLeft
if authData["sort"] == "mostcards":
    games = sorted(badgesLeft, key = lambda value: value[1], reverse = True)
if authData["sort"] == "leastcards":
    games = sorted(badgesLeft, key = lambda value: value[1], reverse = False)

# Start idling games
logger.info("Idle Master needs to idle " + colorGreen + str(len(badgesLeft)) + colorReset + " game(s)")
numSkip = 0
for appID, drops, value in games:
    delay = (int(drops) * 600)
    stillHaveDrops = 1
    numCycles = 50
    maxFail = 2
    skip = False
    openApp = True
    appName = get_app_name(appID)

    while stillHaveDrops == 1:
        try:
            # Sanity check against infinite loop
            if numCycles < 1:
                stillHaveDrops = 0

            # Error Checking
            # Check if cookies still valid or steam is down (network issue)
            expired = cookie_test()
            if expired:
                steamUp = requests.get("https://store.steampowered.com")
                rCode = steamUp.status_code
                if rCode == 200:
                    idle_close(appID, appName)
                    logger.warning(colorYellow + "Cookie session expired" + colorReset)
                    input("Press Enter to continue...")
                    sys.exit()
            else:
                logger.info("Checking to see if " + appName + " has remaining card drops...")
                rBadge = requests.get(myProfileURL + "/gamecards/" + str(appID) + "/", cookies = cookies)
                indBadgeData = bs4.BeautifulSoup(rBadge.text, "html.parser")
                badgeLeftString = indBadgeData.find_all("span", {"class": "progress_info_bold"})[0].contents[0]
                dropCountInt, junk = badgeLeftString.split(" ", 1)
                if dropCountInt.isdigit():
                    dropCountInt = int(dropCountInt)
                    delay = (dropCountInt * 600)
                    logger.info(appName + " has " + colorGreen + str(dropCountInt) + colorReset + " card drops remaining")
                else:
                    logger.info("No card drops remaining")
                    stillHaveDrops = 0
                    break

            if openApp:
                idle_open(appID, appName)
                openApp = False
            ftime = "{:n}".format(delay / 60)
            logger.info("Sleeping for " + str(ftime) + " minutes...")
            time.sleep(delay)
            numCycles -= 1
        except KeyboardInterrupt:
            idle_close(appID, appName)
            logger.warning(colorYellow + "User interrupted script..." + colorReset)

            # Options menu
            ans = True
            while ans:
                print("    q = Quit")
                print("    r = Resume")
                print("    s = Skip game")
                print("    b = Blacklist game")
                print("    w = Whitelist game")

                try:
                    ans = input("Select option (default=r):").strip().lower() or "r"
                except KeyboardInterrupt:
                    ans = "q"
                if ans == "q":
                    logger.warning(colorYellow + "User quit script" + colorReset)
                    sys.exit()
                elif ans == "r":
                    logger.info(colorGreen + "Resuming idling" + colorReset)
                    openApp = True
                    break
                elif ans == "s":
                    logger.warning(colorYellow + "Skipping game" + colorReset)
                    skip = True
                    numSkip += 1
                    break
                elif ans == "b":
                    logger.warning(colorYellow + "Game blacklisted, skipping game" + colorReset)
                    blacklist_game(appID)
                    skip = True
                    numSkip += 1
                    break
                elif ans == "w":
                    logger.warning(colorYellow + "Game whitelisted, skipping game" + colorReset)
                    whitelist_game(appID)
                    skip = True
                    numSkip += 1
                    break
                else:
                    logger.warning(colorYellow + "Invalid option..." + colorReset)
            if skip:
                break
        except SystemExit:
            sys.exit()
        except:
            try:
                if maxFail >= 0:
                    logger.warning(colorYellow + "Steam unreachable or network down, number of tries remaining: " + colorReset + str(maxFail))
                    time.sleep(10)
                    maxFail -= 1
                else:
                    # Suspend operations until Steam can be reached
                    chill_out(appID, appName)
                    maxFail += 1
                    openApp = True
            except SystemExit:
                sys.exit()
            except:
                logger.error(colorRed + "Unknown network issue" + colorReset)
                input("Press Enter to continue...")
                sys.exit()
    if not skip:
        idle_close(appID, appName)
        logger.info(colorGreen + "Successfully completed idling cards for " + appName + colorReset)

# Finish idling
logger.info(colorGreen + "Successfully completed idling process" + colorReset)
logger.warning(colorYellow + str(numSkip) + " game(s) skipped" + colorReset)
input("Press Enter to continue...")