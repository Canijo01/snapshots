import configparser
import os
from  obtentoken import *
from snapshots import *
import json
import asyncio
import aiohttp

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
user_data = ""

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

instantaneas_array = []
for secciones in instantaneas.sections():
    for variable in instantaneas.items(secciones):
        exec(f"{variable[0]}=\"{variable[1]}\"")
        # print(f"{variable[0]}=\"{variable[1]}\"")
        all_vms_disks = bool(all_vms_disks)
    instantaneas_array.append({
        'disk_id': "%s" % (disk_id),
        'disk_name': "%s" % (disk_name),
        'disk_description': "%s" % (disk_description),
        'snapshot_id': "%s" % (snapshot_id),
        'snaphot_name': "%s" % (snapshot_name),
        'all_vms_disks': "%s" % (all_vms_disks),
    })


config = configparser.ConfigParser()
a = config.read("config.ini")
# for i in os.environ:
#    print (i,os.environ[i])
if "APPID" in os.environ:
    APP_ID = os.environ['APPID']
    print("APP_ID:Ok")
if "SECRET" in os.environ:
    SECRET = os.environ['SECRET']
    print("SECRET:Ok")

CUSTOMER_ID = config.get("AMX", "CUSTOMER_ID")
CLOUDSPACE_ID = config.get("AMX", "CLOUDSPACE_ID")
LOCATION = config.get("AMX", "LOCATION")
TOKEN = config.get("AMX", "TOKEN")
URL = config.get("AMX", "URL")
DEPLOY = config.get("AMX", "DEPLOY")
SNAPSHOTS = config.get("AMX", "SNAPSHOTS")
#######
#
# Abir el archivo donde estan descitas las VMs acrear
#
deploy = configparser.ConfigParser()
d = deploy.read(DEPLOY)
### Esta linea es para conservar las mayusculas. Normalmente convierte a minusculas
deploy.optionxform = str
### Estas lineas son para que no marque errores el ambiente de desarrollo al no estar las variables definidas.

name = ""  # nombre de la vm a crear
description = ""
vcpus = 1  # vcpus a utilizar 1 a 64
memory = 512  # memoria en multiplos de 128. Maximo 131072 (128Gb)
private_ip = "192.168.103.1"  # ip de la vm
image_id = 1
os_name = ""
disk_size = 10

# token = get_token(APP_ID, SECRET, IYO_URL)
jH = get_headers_js(TOKEN)
resultados=[]
tasks=[]
datas=[]
inicio = time.time()

print(f'Secciones es de este tamaño: {len(deploy.sections())}')
for secciones in deploy.sections():
    data_disks=""
    data_disks_array=[]
    externalnetworks=""
    externalnetworks_array=[]
    #print (f'Seccion a trabajar: {secciones}')
    for variable in deploy.items(secciones):
        exec(f"{variable[0]} = '{variable[1]}'")
        #exec (f"print(f'{variable[0]} = {variable[1]}')")
    #print(f'name = {name}')
    if (data_disks):
        for x in data_disks.split(","):
            data_disks_array.append(int(x))
    if (externalnetworks):
        for x in externalnetworks.split(","):
            externalnetworks_array.append(x.split(":"))
    if ( image_id == "215"):
        user_data = "users: [{name: Administrator, primary_group: Administrators, passwd: Astellia123, inactive: false}, {name: exfo, primary_group: Users, groups: Administrators, passwd: Astellia123, inactive: false}]"
    else:
        user_data = "users: [{default},{name: exfo, shell: /bin/bash, plain_text_passwd: Astellia123, lock_passwd: False}, {name: root, plain_text_passwd: +Passw0rd@stellia, shell: /bin/bash, lock_passwd: False}]"

    data =[ {
        'name': f'{name}',
        'description': f'{description}',
        'vcpus': f'{vcpus}',
        'memory': f'{memory}',
        'image_id': f'{image_id}',
        'private_ip': f'{private_ip}',
        'os_type': f'{os_type}',
        'os_name': f'{os_name}',
        'user_data' : f'{user_data}',
        'disk_size': f'{disk_size}',
        'data_disks': data_disks_array,
        #'disk_id': "%s" % (disk_id),
        #'disk_name': "%s" % (disk_name),
        #'disk_description': "%s" % (disk_description),
    #    'snapshot_id': "%s" % (snapshot_id),
    #    'snapshot_name': "%s" % (snapshot_name),
    #    'all_vm_disks': "%s" % (all_vms_disks),

    },externalnetworks_array]
    datas.append(data)
Ahora = time.time()
async def deploy(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,datas):
    for data in datas:
        print(json.dumps(data[0],indent=4))
    #print(clone_machine_from_disk_id(jH, URL, CUSTOMER_ID, CLOUDSPACE_ID, LOCATION, data))
    #print(deploy_vm_from_image_id(jH, URL, CUSTOMER_ID, CLOUDSPACE_ID, data))


    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=5)) as session:
        for data in datas:

            tasks.append(asyncio.ensure_future(deploy_vm_from_image_id(session,
                                                                        jH,
                                                                        URL,
                                                                        CUSTOMER_ID,
                                                                        CLOUDSPACE_ID,
                                                                        data)))
        results = await asyncio.gather(*tasks)
   #results = await asyncio.gather(*tasks)


async def main():
    first=0
    last=0
    batch = 0
    while datas:
root

        batch += 1
        print(f'Batch: {batch} de vm {first} hasta {last} ')
        x = datas[first:last]
        first=last
        await deploy(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,x)
        print("Segundos transcuridos: %ss Total %s" % (time.time() - Ahora,time.time() - inicio))
    await asyncio.sleep(60)
    print("Rutina Terminada")
asyncio.run(main())