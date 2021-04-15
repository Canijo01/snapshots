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
EXPORTS = config.get("AMX", "EXPORTS")
IMPORTS = config.get("AMX", "IMPORTS")
S3LINK = config.get("AMX", "S3LINK")
S3BUCKET = config.get("AMX", "S3BUCKET")
S3KEY = config.get("AMX", "S3KEY")
S3SECRET = config.get("AMX", "S3SECRET")
S3REGION = config.get("AMX", "S3REGION")

####
#
#  Abrir la información de los snapshots. Ya que npo se pueden borrar se modifico el programa para leerlos desde
# un ini file descrito eb la variable SNAPSHOTS
#
#

#######
#
# Abir el archivo donde estan descitas las VMs exportar
#
deploy = configparser.ConfigParser()
d = deploy.read(EXPORTS)
### Esta linea es para conservar las mayusculas. Normalmente convierte a minusculas
deploy.optionxform = str
### Estas lineas son para que no marque errores el ambiente de desarrollo al no estar las variables definidas.

vm_id = ""  # id_de la vm a exportar
object_name = ""

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

for secciones in deploy.sections():
    for variable in deploy.items(secciones):
        exec(f"{variable[0]}=\"{variable[1]}\"")

    data = {
        'link': "%s" % (S3LINK),
        'key': "%s" %(S3KEY),
        'secret': "%s" % (S3SECRET),
        'region': "%s" % (S3REGION),
        'bucket': "%s" % (S3BUCKET),
        'object_name': "%s" % (object_name),
            }
    print(json.dumps(data,indent=4))
    Ahora = time.time()
    vm_export_s3(jH, URL, CUSTOMER_ID, CLOUDSPACE_ID, vm_id, data)
    print("Segundos transcuridos: %ss" % (time.time() - Ahora))