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
from colorama import init, Fore, Back, Style

init()

version = "v1.3"

os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

logging.basicConfig(filename="idlemaster.log",filemode="w",format="[ %(asctime)s ] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p",level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(logging.Formatter("[ %(asctime)s ] %(message)s", "%m/%d/%Y %I:%M:%S %p"))
logging.getLogger('').addHandler(console)

if sys.platform.startswith('win32'):
    ctypes.windll.kernel32.SetConsoleTitleA("Idle Master")

logging.warning(Fore.GREEN + "WELCOME TO IDLE MASTER - " + Fore.YELLOW + version + Fore.RESET)

try:
    authData={}
    authData["sort"]=""
    authData["steamparental"]=""
    authData["hasPlayTime"]="false"
    exec(open("./settings.txt").read(),authData)
    myProfileURL = "https://steamcommunity.com/profiles/"+authData["steamLoginSecure"][:17]
except:
    logging.warning(Fore.RED + "Error loading config file" + Fore.RESET)
    input("Press Enter to continue...")
    sys.exit()
    
if not authData["sessionid"]:
    logging.warning(Fore.RED + "No sessionid set" + Fore.RESET)
    input("Press Enter to continue...")
    sys.exit()
    
if not authData["steamLoginSecure"]:
    logging.warning(Fore.RED + "No steamLogin set" + Fore.RESET)
    input("Press Enter to continue...")
    sys.exit()

def generateCookies():
    global authData
    try:
        cookies = dict(sessionid=authData["sessionid"], steamLoginSecure=authData["steamLoginSecure"], steamparental=authData["steamparental"])
    except:
        logging.warning(Fore.RED + "Error setting cookies" + Fore.RESET)
        input("Press Enter to continue...")
        sys.exit()

    return cookies

def dropDelay(numDrops):
    if numDrops>1:
        baseDelay = (15*60)
    else:
        baseDelay = (5*60)
    return baseDelay
    
def idleOpen(appID):
    try:
        logging.warning("Starting game " + getAppName(appID) + " to idle cards")
        global process_idle
        global idle_time

        idle_time = time.time()

        if sys.platform.startswith('win32'):
            process_idle = subprocess.Popen("steam-idle.exe "+str(appID))
        elif sys.platform.startswith('darwin'):
            process_idle = subprocess.Popen(["./steam-idle", str(appID)])
        elif sys.platform.startswith('linux'):
            process_idle = subprocess.Popen(["python", "steam-idle.py", str(appID)])
    except:
        logging.warning(Fore.RED + "Error launching steam-idle with game ID " + str(appID) + Fore.RESET)
        input("Press Enter to continue...")
        sys.exit()

def idleClose(appID):
    try:
        logging.warning("Closing game " + getAppName(appID))
        process_idle.terminate()
        total_time = int(time.time() - idle_time)
        logging.warning(getAppName(appID) + " idled for " + Fore.GREEN + str(datetime.timedelta(seconds=total_time)) + Fore.RESET)
    except:
        logging.warning(Fore.RED + "Error closing game. Exiting." + Fore.RESET)
        input("Press Enter to continue...")
        sys.exit()

def chillOut(appID):
    logging.warning("Suspending operation for "+getAppName(appID))
    idleClose(appID)
    stillDown = True
    while stillDown:
        logging.warning("Sleeping for 5 minutes.")
        time.sleep(5*60)
        try:
            rBadge = requests.get(myProfileURL+"/gamecards/" + str(appID) + "/",cookies=cookies)
            indBadgeData = bs4.BeautifulSoup(rBadge.text, "html.parser")
            badgeLeftString = indBadgeData.find_all("span",{"class": "progress_info_bold"})[0].contents[0]
            if badgeLeftString:
                stillDown = False
        except:
            logging.warning("Still unable to find drop info.")
    # Resume operations.
    idleOpen(appID)

def getAppName(appID):
    try:
        api = requests.get("https://store.steampowered.com/api/appdetails/?appids=" + str(appID) + "&filters=basic")
        api_data = json.loads(api.text)
        return Fore.CYAN + api_data[str(appID)]["data"]["name"].encode('ascii', 'ignore') + Fore.RESET
    except:
        return Fore.CYAN + "App "+str(appID) + Fore.RESET

def getPlainAppName(appid):
    try:
        api = requests.get("https://store.steampowered.com/api/appdetails/?appids=" + str(appID) + "&filters=basic")
        api_data = json.loads(api.text)
        return api_data[str(appID)]["data"]["name"].encode('ascii', 'ignore')
    except:
        return "App "+str(appID)

def get_blacklist():
    try:
        with open('blacklist.txt', 'r') as f:
            lines = f.readlines()
        blacklist = [int(n.strip()) for n in lines]
    except:
        blacklist = [];

    if not blacklist:
        logging.warning("No games have been blacklisted")

    return blacklist

logging.warning("Finding games that have card drops remaining")

try:
    cookies = generateCookies()
    r = requests.get(myProfileURL+"/badges/",cookies=cookies)
except:
    logging.warning(Fore.RED + "Error reading badge page" + Fore.RESET)
    input("Press Enter to continue...")
    sys.exit()

try:
    badgesLeft = []
    badgePageData = bs4.BeautifulSoup(r.text, "html.parser")
    badgeSet = badgePageData.find_all("div",{"class": "badge_title_stats"})
except:
    logging.warning(Fore.RED + "Error finding drop info" + Fore.RESET)
    input("Press Enter to continue...")
    sys.exit()

# For profiles with multiple pages
try:
    badgePages = int(badgePageData.find_all("a",{"class": "pagelink"})[-1].text)
    if badgePages:
        logging.warning(str(badgePages) + " badge pages found.  Gathering additional data")
        currentpage = 2
        while currentpage <= badgePages:
            r = requests.get(myProfileURL+"/badges/?p="+str(currentpage),cookies=cookies)
            badgePageData = bs4.BeautifulSoup(r.text, "html.parser")
            badgeSet = badgeSet + badgePageData.find_all("div",{"class": "badge_title_stats"})
            currentpage = currentpage + 1
except:
    logging.warning("Reading badge page, please wait")

userinfo = badgePageData.find("a",{"class": "user_avatar"})
if not userinfo:
    logging.warning(Fore.RED + "Invalid cookie data, cannot log in to Steam" + Fore.RESET)
    input("Press Enter to continue...")
    sys.exit()

blacklist = get_blacklist()

if authData["sort"]=="mostvalue" or authData["sort"]=="leastvalue":
    logging.warning("Getting card values, please wait...")

for badge in badgeSet:

    try:
        badge_text = badge.get_text()
        dropCount = badge.find_all("span",{"class": "progress_info_bold"})[0].contents[0]
        has_playtime = re.search("[0-9\.] hrs on record", badge_text) != None

        if "No card drops" in dropCount or (has_playtime == False and authData["hasPlayTime"].lower() == "true") :
            continue
        else:
            # Remaining drops
            dropCountInt, junk = dropCount.split(" ",1)
            dropCountInt = int(dropCountInt)
            linkGuess = badge.find_parent().find_parent().find_parent().find_all("a")[0]["href"]
            junk, badgeId = linkGuess.split("/gamecards/",1)
            badgeId = int(badgeId.replace("/",""))
            if badgeId in blacklist:
                logging.warning(getAppName(badgeId) + " on blacklist, skipping game")
                continue
            else:
                if authData["sort"]=="mostvalue" or authData["sort"]=="leastvalue":
                    api = requests.get("https://api.augmentedsteam.com/v2/market/cards/average-prices/?appids=" + str(badgeId) + "&currency=usd")
                    api_data = json.loads(api.text)

                    if api.text.find('regular') == -1:
                        logging.warning("No card data for" + Fore.CYAN + " App " + str(badgeId) + Fore.RESET + " skipping...")
                        gameValue = "0"
                    else:
                        gameValue = api_data['data'][str(badgeId)]['regular']

                    push = [badgeId, dropCountInt, float(str(gameValue))]
                    badgesLeft.append(push)
                else:
                    push = [badgeId, dropCountInt, 0]
                    badgesLeft.append(push)
    except:
        continue

logging.warning("Idle Master needs to idle " + Fore.GREEN + str(len(badgesLeft)) + Fore.RESET + " games")

def getKey(item):
    if authData["sort"]=="mostcards" or authData["sort"]=="leastcards":
        return item[1]
    elif authData["sort"]=="mostvalue" or authData["sort"]=="leastvalue":
        return item[2]
    else:
        return item[0]

sortValues = ["", "mostcards", "leastcards", "mostvalue", "leastvalue"]
if authData["sort"] in sortValues:
    if authData["sort"]=="":
        games = badgesLeft
    if authData["sort"]=="mostcards" or authData["sort"]=="mostvalue":
        games = sorted(badgesLeft, key=getKey, reverse=True)
    if authData["sort"]=="leastcards" or authData["sort"]=="leastvalue":
        games = sorted(badgesLeft, key=getKey, reverse=False)
else:
    logging.warning(Fore.RED + "Invalid sort value" + Fore.RESET)
    input("Press Enter to continue...")
    sys.exit()

for appID, drops, value in games:
    delay = dropDelay(int(drops))
    stillHaveDrops=1
    numCycles=50
    maxFail=2
    
    idleOpen(appID)

    logging.warning(getAppName(appID) + " has " + str(drops) + " card drops remaining")

    if sys.platform.startswith('win32'):
        ctypes.windll.kernel32.SetConsoleTitleA("Idle Master - Idling " + getPlainAppName(appID) + " [" + str(drops) + " remaining]")

    while stillHaveDrops==1:
        try:
            logging.warning("Sleeping for " + str(delay / 60) + " minutes")
            time.sleep(delay)
            numCycles-=1
            if numCycles<1: # Sanity check against infinite loop
                stillHaveDrops=0

            logging.warning("Checking to see if " + getAppName(appID) + " has remaining card drops")
            rBadge = requests.get(myProfileURL + "/gamecards/" + str(appID) + "/",cookies=cookies)
            indBadgeData = bs4.BeautifulSoup(rBadge.text, "html.parser")
            badgeLeftString = indBadgeData.find_all("span",{"class": "progress_info_bold"})[0].contents[0]
            dropCountInt, junk = badgeLeftString.split(" ",1)
            if dropCountInt.isdigit():
                dropCountInt = int(dropCountInt)
                delay = dropDelay(dropCountInt)
                logging.warning(getAppName(appID) + " has " + str(dropCountInt) + " card drops remaining")
                if sys.platform.startswith('win32'):
                    ctypes.windll.kernel32.SetConsoleTitleA("Idle Master - Idling " + getPlainAppName(appID) + " [" + str(dropCountInt) + " remaining]")
            else:
                logging.warning("No card drops remaining")
                stillHaveDrops=0
        except KeyboardInterrupt:
            idleClose(appID)
            logging.warning("User interrupted script. Exiting")
            sys.exit()
        except:
            if maxFail>0:
                logging.warning("Error checking if drops are done, number of tries remaining: " + str(maxFail))
                maxFail-=1
            else:
                # Suspend operations until Steam can be reached.
                chillOut(appID)
                maxFail+=1

    idleClose(appID)
    logging.warning(Fore.GREEN + "Successfully completed idling cards for " + getAppName(appID) + Fore.RESET)

logging.warning(Fore.GREEN + "Successfully completed idling process" + Fore.RESET)
input("Press Enter to continue...")