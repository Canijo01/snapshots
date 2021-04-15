import configparser
import os
import json
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
CLOUDSPACE_ID = config.get("AMX", "CLOUDSPACE_ID")
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
#print(snapshotcloudspaces2(jH,URL,CUSTOMER_ID))
#clone_machine_in_cloudspace(jH, URL,CUSTOMER_ID,CLOUDSPACE_ID,LOCATION)
boot_disk_id=1612
disk_id="1341"
disk_name="Exfo_CentOS7_NovaSmall_v7.7.0.0"
disk_description="Exfo_CentOS7_NovaSmall_v7.7.0.0"
os_type="Linux"
name="vm_4_clone"
description=disk_description
vcpus="1"
memory="512"
private_ip="192.168.103.104"
data_disks=["100","100"]
data_disks_one_disk=["11"]
data_disks_two_disks=["11","21"]
disk1="11"
disk2="12"
all_vm_disks=True
data = {
                'name': "%s" % (name),
                'description': "%s" % (description),
                'vcpus': "%s" % (vcpus),
                'memory': "%s" %(memory),
                'private_ip': "%s" % (private_ip),
                'os_type': "%s" % (os_type),
                'data_disks': "%s" % (data_disks),
                'disk_id': "%s" % (disk_id),
                'disk_name': "%s" % (disk_name),
                'disk_description': "%s" % (disk_description),
                'all_vm_disks': "%s" %(all_vm_disks)

}
vm_data= {
            'name': "%s" % (name),
            'description': "%s" % (description),
            'vcpus': "%s" % (vcpus),
            'memory': "%s" %(memory),
            'private_ip': "%s" % (private_ip),
            'boot_disk_id': "%s" % (boot_disk_id),
            'os_type': "%s" % (os_type),
            #'data_disks': ["%s" %(disk1),"%s" %(disk2)]  #Doesnt work
            #'data_disks': data_disks_two_disks  #Doesnt work
            #'data_disks':["10","11"] #doesnt work
            #'data_disks':[10,11] #doesnt work
            #'data_disks': ["%s" %(disk1)] #works
            #'data_disks': data_disks_one_disk #works
            #'data_disks':["10"] #works
            #'data_disks':[10] #works
            'data_disks':[10] #works

}
print(json.dumps(vm_data,indent=4))
#print(vm_create(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,vm_data))
print(clone_machine_from_disk_id(jH, URL,CUSTOMER_ID,CLOUDSPACE_ID,LOCATION,data))
#print(snapshotcloudspaces(jH,URL3))