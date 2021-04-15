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


CUSTOMER_ID = config.get("AMX", "CUSTOMER_ID")
LOCATION = config.get("AMX", "LOCATION")
TOKEN = config.get("AMX", "TOKEN")
#URL = config.get("LOCATIONS", "URL")
URL = config.get("AMX", "URL")
#URL3 = config.get("LOCATIONS", "URL3")


#token = get_token(APP_ID, SECRET, IYO_URL)
jH = get_headers_js(TOKEN)
oH = get_headers_os(TOKEN)
#print(snapshotcloudspaces(jH,URL))
print (jH)

def get_me(headers, URL):
    data = {}
    api_get = 'api/1/me'
    cloudspace = requests.get(URL + api_get, headers=headers)

    return (cloudspace)

def get_locations(headers, URL):
    data = {}
    api_get = 'api/1/locations'
    cloudspace = requests.get(URL + api_get, headers=headers)

    return (cloudspace)
def get_customers(headers, URL):
    data = {}
    api_get = 'api/1/customers'
    cloudspace = requests.get(URL + api_get, headers=headers)

    return (cloudspace)
def get_customers_cloudspaces(headers, URL,customer_id):
    data = {
        'include_deleted': True,
        'location':""
    }
    api_get = 'api/1/customers/%s/cloudspaces'%(customer_id)
    cloudspace = requests.get(URL + api_get, headers=headers,params=data)

    return (cloudspace)

print(get_customers_cloudspaces(jH,URL,CUSTOMER_ID).text)