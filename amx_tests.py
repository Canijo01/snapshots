import configparser
import os
from  obtentoken import *
import asyncio
from snapshots import *
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

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

#print(stop_vms_cloudspaces(jH,URL,CUSTOMER_ID,True))
#asyncio.run(stop_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True))
asyncio.run( get_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID))
#Advertencia vm_id: 3338 no se pudo detener información. Mensaje: {'message': 'Something bad happened. Contact support and pass them "4647bd0c544ac94c8ab575bd34d13feb-1619022816.048166"', 'errorcode': '4647bd0c544ac94c8ab575bd34d13feb-1619022816.048166'}
# api_get api/1/customers/exfo_1/cloudspaces/dXMtamFjLWRjMDEtMDAyOjEzMDI/vms/3338

result = vm_get(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,"3338")
#await result.json()#print(stop_vms_cloudspaces(jH,URL,CUSTOMER_ID,True))
#
#print(delete_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True))
#asyncio.run(delete_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True))
#print( vm_create(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,data))
#print(snapshotcloudspaces(jH,URL3))

ndays=1
dEpoch = timedelta(days=ndays)
#dEpoch = timedelta(minutes=60)

ahora = datetime.utcnow()
end = int(time.mktime(ahora.timetuple()))
start = int(time.mktime((ahora-dEpoch).timetuple()))
print (end,start)
consumption = get_consumption_cloudspace(jH, URL,CUSTOMER_ID,CLOUDSPACE_ID,start,end)

print(consumption.json()["cloudspace"]["consumption"])
for vms in consumption.json()["cloudspace"]["vms"]:
    print (vms["consumption"])
