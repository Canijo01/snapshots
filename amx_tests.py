import configparser
import os
from  obtentoken import *
from snapshots import *
from datetime import datetime, timedelta
import json

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
CLOUDSPACE_ID = config.get("AMX", "CLOUDSPACE_ID")
LOCATION = config.get("AMX", "LOCATION")
TOKEN = config.get("AMX", "TOKEN")
URL = config.get("AMX", "URL")


data = {
    'name': "%s" % (config.get("Machine1", "NAME")),
    'description': "%s" % (config.get("Machine1", "DESCRIPTION")),
    'disk_size': "%s" % (config.get("Machine1", "DISK_SIZE")),
    #'data_disks': "%s" % (config.get("Machine1", "DATA_DISKS")),
    'vcpus': "%s" % (config.get("Machine1", "VCPUS")),
    'memory': "%s" % (config.get("Machine1", "MEMORY")),
    'private_ip': "%s" % (config.get("Machine1", "PRIVATE_IP")),
    'image_id': "%s" % (config.get("Machine1", "IMAGE_ID")),
    'os_type': "%s" % (config.get("Machine1", "OS_TYPE"))
}
#token = get_token(APP_ID, SECRET, IYO_URL)
jH = get_headers_js(TOKEN)
oH = get_headers_os(TOKEN)
#print(snapshotcloudspaces(jH,URL))
print (jH)
print(stop_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True))
#print(stop_vms_cloudspaces(jH,URL,CUSTOMER_ID,True))
#
print(delete_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True))
#print( vm_create(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,data))
#print(snapshotcloudspaces(jH,URL3))

ndays=1
dEpoch = timedelta(days=ndays)
ahora = datetime.utcnow()
end = int(time.mktime(ahora.timetuple()))
start = int(time.mktime((ahora-dEpoch).timetuple()))
print (end,start)
consumption = get_consumption_cloudspace(jH, URL,CUSTOMER_ID,CLOUDSPACE_ID,start,end)

print(consumption.json()["cloudspace"]["consumption"])
for vms in consumption.json()["cloudspace"]["vms"]:
    print (vms["consumption"])
