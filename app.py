import configparser
import os
from  obtentoken import *
from snapshots import *

config = configparser.ConfigParser()
a = config.read("config.ini")
for i in os.environ:
    print (i,os.environ[i])
APP_ID = os.environ['iyo-app']
SECRET = os.environ['iyo-secret']
#APP_ID = config.get("ACCESS", "APP_ID")
#SECRET = config.get("ACCESS", "Secret")
IYO_URL = config.get("ACCESS", "IYO_URL")
URL = config.get("LOCATIONS", "URL")
URL2 = config.get("LOCATIONS", "URL2")
URL3 = config.get("LOCATIONS", "URL3")

Intervalo = 1  #minutos
multiplier = 1   #minutos
time_range = int( Intervalo / multiplier)
sleep_delay = int(60 * multiplier)
#print (sleep_delay)

while True:
    token = get_token(APP_ID, SECRET, IYO_URL)
    jH = get_headers_js(token)
    oH = get_headers_os(token)
    for i in range(time_range):
        print("Dumiendo, en %s minutos despierto para hacer snaps en %s" % ((time_range -  i) * multiplier ,URL))
        time.sleep(sleep_delay) # Delay for 1 minute (60 seconds).
    print(snapshotcloudspaces(jH,URL))
    for i in range(time_range):
        print("Dumiendo, en %s minutos despierto para hacer snaps en %s" % ((time_range -  i) * multiplier ,URL2))
        time.sleep(sleep_delay) # Delay for 1 minute (60 seconds).
    print(snapshotcloudspaces(jH,URL2))
    for i in range(sleep_delay):
        print("Dumiendo, en %s minutos despierto para hacer snaps en %s" % ((time_range -  i) * multiplier ,URL3))
        time.sleep(sleep_delay) # Delay for 1 minute (60 seconds).
    print(snapshotcloudspaces(jH,URL3))
