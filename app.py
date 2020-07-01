import configparser
from  obtentoken import *
from snapshots import *

config = configparser.ConfigParser()
a = config.read("config.ini")

APP_ID = config.get("ACCESS", "APP_ID")
SECRET = config.get("ACCESS", "Secret")
IYO_URL = config.get("ACCESS", "IYO_URL")
URL = config.get("LOCATIONS", "URL")
URL2 = config.get("LOCATIONS", "URL2")
URL3 = config.get("LOCATIONS", "URL3")

token = get_token(APP_ID, SECRET, IYO_URL)
jH = get_headers_js(token)
oH = get_headers_os(token)
while True:
    for i in range(470):
        print("Dumiendo, en %s minutos despierto para hacer snaps en %s" % (470 - i,URL))
        time.sleep(60) # Delay for 1 minute (60 seconds).
    print(snapshotcloudspaces(jH,URL))
    for i in range(470):
        print("Dumiendo, en %s minutos despierto para hacer snaps en %s" % (470 - i,URL2))
        time.sleep(60) # Delay for 1 minute (60 seconds).
    print(snapshotcloudspaces(jH,URL2))
    for i in range(470):
        print("Dumiendo, en %s minutos despierto para hacer snaps en %s" % (470 - i,URL3))
        time.sleep(60) # Delay for 1 minute (60 seconds).
    print(snapshotcloudspaces(jH,URL3))
