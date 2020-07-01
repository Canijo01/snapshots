import configparser
import time
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



