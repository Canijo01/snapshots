import configparser
import os
from  obtentoken import *
from snapshots import *
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
DEPLOY = config.get("AMX", "DEPLOY")
SNAPSHOTS = config.get("AMX", "SNAPSHOTS")
####
#
#  Abrir la información de los snapshots. Ya que npo se pueden borrar se modifico el programa para leerlos desde
# un ini file descrito eb la variable SNAPSHOTS
#
#
instantaneas = configparser.ConfigParser()
i = instantaneas.read(SNAPSHOTS)
### Esta linea es para conservar las mayusculas. Normalmente convierte a minusculas
instantaneas.optionxform = str
### Estas lineas son para que no marque errores el ambiente de desarrollo al no estar las variables definidas.
disk_id= ""
snapshot_id = ""
snapshot_name = ""
disk_name = "" # Nombre que tendra el disco. Normalmente la version de SO a utilizar
disk_description = "" #Normalmente la version de S.O. a utilizar
all_vms_disks = True # Parametro cuando se hace el snapshot
os_type = "" # opciones Linux Windows

#######
#
# Abir el archivo donde estan descitas las VMs acrear
#
deploy = configparser.ConfigParser()
d = deploy.read(DEPLOY)
### Esta linea es para conservar las mayusculas. Normalmente convierte a minusculas
deploy.optionxform = str
### Estas lineas son para que no marque errores el ambiente de desarrollo al no estar las variables definidas.

name = "VM_001"  # nombre de la vm a crear
description="NORMALY_DISK_DESCRIPTION"
vcpus = 1  # vcpus a utilizar 1 a 64
memory = 512 # memoria en multiplos de 128. Maximo 131072 (128Gb)
private_ip = "192.168.103.1" #ip de la vm

#token = get_token(APP_ID, SECRET, IYO_URL)
jH = get_headers_js(TOKEN)
oH = get_headers_os(TOKEN)
#print(snapshotcloudspaces(jH,URL))
#print (jH)
#print(stop_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True))
#print(stop_vms_cloudspaces(jH,URL,CUSTOMER_ID,True))
#print(delete_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True))
#print( vm_create(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,data))
#print(snapshotcloudspaces(jH,URL3))

#######
##Loop principal
##
##
## Lee los párametros de las vms del archivo de configuracion
### Estas se cargan del archivo de configuración vm_deploy.ini
### Inicia la creación al clonar desde el disco indicado y encender la máquina con las caracteristicas solicitadas
###
###
instantaneas_array=[]
for secciones in instantaneas.sections():
    for variable in instantaneas.items(secciones):
        exec(f"{variable[0]}=\"{variable[1]}\"")
        #print(f"{variable[0]}=\"{variable[1]}\"")
        all_vms_disks=bool(all_vms_disks)
    instantaneas_array.append( {
        'disk_id': "%s" % (disk_id),
        'disk_name': "%s" % (disk_name),
        'disk_description': "%s" % (disk_description),
        'snapshot_id': "%s" % (snapshot_id),
        'snaphot_name': "%s" % (snapshot_name),
        'all_vms_disks': "%s" % (all_vms_disks),
            })
#print(json.dumps(instantaneas_array, indent=4))
resultados=[]
inicio = time.time()
for secciones in deploy.sections():
    data_disks=""
    data_disks_array=[]
    externalnetworks=""
    externalnetworks_array=[]
    for variable in deploy.items(secciones):
        exec(f"{variable[0]}=\"{variable[1]}\"")
    if (data_disks):
        for x in data_disks.split(","):
            data_disks_array.append(int(x))
    if (externalnetworks):
        for x in externalnetworks.split(","):
            externalnetworks_array.append(x.split(":"))
    #for from_instantaneas in instantaneas_array:
    #    if (from_instantaneas["disk_id"] == disk_id):
    #        snapshot_id=from_instantaneas["snapshot_id"]
    #        snapshot_name=from_instantaneas["snaphot_name"]
    #        disk_name = from_instantaneas["disk_name"]
    #        disk_description = from_instantaneas["disk_description"]
    #        all_vms_disks = from_instantaneas["all_vms_disks"]
    data = {
        'name': "%s" % (name),
        'description': "%s" %(description),
        'vcpus': "%s" % (vcpus),
        'memory': "%s" % (memory),
        'image_id': "%s" % (image_id),
        'private_ip': "%s" % (private_ip),
        'os_type': "%s" % (os_type),
        'os_name': "%s" % (os_name),
        'disk_size': "%s" %(disk_size),
        'data_disks': data_disks_array,
        #'disk_id': "%s" % (disk_id),
        #'disk_name': "%s" % (disk_name),
        #'disk_description': "%s" % (disk_description),
    #    'snapshot_id': "%s" % (snapshot_id),
    #    'snapshot_name': "%s" % (snapshot_name),
    #    'all_vm_disks': "%s" % (all_vms_disks),
        'externalnetworks':externalnetworks_array
    }
    print(json.dumps(data,indent=4))
    #print(clone_machine_from_disk_id(jH, URL, CUSTOMER_ID, CLOUDSPACE_ID, LOCATION, data))
    #print(deploy_vm_from_image_id(jH, URL, CUSTOMER_ID, CLOUDSPACE_ID, data))
    Ahora = time.time()
    resultados.append(deploy_vm_from_image_id(jH, URL, CUSTOMER_ID, CLOUDSPACE_ID, data))
    print("Segundos transcuridos: %ss Total %s" % (time.time() - Ahora,time.time() - inicio))
for r in resultados:
    print(r.text)