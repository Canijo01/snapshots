import configparser
import os
from  obtentoken import *
from snapshots import *

config = configparser.ConfigParser()
a = config.read("config.ini")
#for i in os.environ:
#    print (i,os.environ[i])
if "APPID" in os.environ:
    APP_ID = os.environ['APPID']
    print ("APP_ID:Ok")
if "SECRET" in os.environ:
    SECRET = os.environ['SECRET']
    print("SECRET:Ok" )


APP_ID = config.get("ACCESS", "APP_ID")
SECRET = config.get("ACCESS", "Secret")
IYO_URL = config.get("ACCESS", "IYO_URL")
#URL = config.get("LOCATIONS", "URL")
URL2 = config.get("LOCATIONS", "URL2")
#URL3 = config.get("LOCATIONS", "URL3")


token = get_token(APP_ID, SECRET, IYO_URL)
jH = get_headers_js(token)
oH = get_headers_os(token)
#print(snapshotcloudspaces(jH,URL))
print (token)
print(snapshotcloudspaces(jH,URL2))


#print(snapshotcloudspaces(jH,URL3))