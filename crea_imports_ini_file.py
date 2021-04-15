import configparser
import os

config = configparser.ConfigParser()
a = config.read("config.ini")

CUSTOMER_ID = config.get("AMX", "CUSTOMER_ID")
CLOUDSPACE_ID = config.get("AMX", "CLOUDSPACE_ID")
LOCATION = config.get("AMX", "LOCATION")
TOKEN = config.get("AMX", "TOKEN")
URL = config.get("AMX", "URL")
DEPLOY = config.get("AMX", "DEPLOY")
#######
#
# Abir el archivo donde estan descitas las VMs acrear
#
deploy = configparser.ConfigParser()
d = deploy.read(DEPLOY)
### Esta linea es para conservar las mayusculas. Normalmente convierte a minusculas
deploy.optionxform = str
### Estas lineas son para que no marque errores el ambiente de desarrollo al no estar las variables definidas.
replicas = 0
vms =  0 # Numero de vms a Crear
name = "VM_001"  # nombre de la vm a crear
description="NORMALY_DISK_DESCRIPTION"
vcpus = 1  # vcpus a utilizar 1 a 64
memory = 512 # memoria en multiplos de 128. Maximo 131072 (128Gb)
private_ip = "192.168.103.1" #ip de la vm
externalnetworks = ""
contador_maestro = 0
arreglo_maestro = ""
ip_array=[]
for secciones in deploy.sections():
    #print(deploy.items(secciones))
    for variable in deploy.items(secciones):
        exec(f"{variable[0]}=\"{variable[1]}\"")
        #print (variable)
    ip_array=private_ip.split(".")
    for contador_vms in range(int(replicas)):
        arreglo_maestro=arreglo_maestro+("\n[%s-%s]\n"%(secciones,contador_vms))
        if int(replicas) == 1:
            arreglo_maestro = arreglo_maestro + ("name = %s\n" % (name))
        else:
            if contador_vms < 9:
                arreglo_maestro = arreglo_maestro+("name = %s00%s\n" % (name, contador_vms+1))
            else:
                arreglo_maestro = arreglo_maestro + ("name = %s0%s\n" % (name, contador_vms+1))
        for variable in deploy.items(secciones):
            if variable[0] not in ["name", "replicas","private_ip","externalnetworks"]:
                arreglo_maestro = arreglo_maestro+("%s = %s\n" % (variable[0], variable[1]))
            else:
                if variable[0]  in ["private_ip"]:
                    arreglo_maestro = arreglo_maestro \
                                      +("%s = %s.%s.%s.%s\n"
                                        %(variable[0], ip_array[0],ip_array[1],ip_array[2],int(ip_array[3])+contador_vms))
                if variable[0] in ["externalnetworks"]:
                    new_ext_network=""
                    for redes in externalnetworks.split(","):
                        binomio = redes.split(":")
                        ip_en= binomio[1].split(".")
                        if new_ext_network == "":
                            new_ext_network = new_ext_network + ("%s:%s.%s.%s.%s"
                                                                 %(binomio[0],ip_en[0],ip_en[1],ip_en[2],int(ip_en[3])+contador_vms))
                        else:
                            new_ext_network = new_ext_network + (",%s:%s.%s.%s.%s"
                                                                 % (binomio[0], ip_en[0], ip_en[1], ip_en[2], int(ip_en[3]) + contador_vms))
                    arreglo_maestro = arreglo_maestro + ("%s = %s\n" % (variable[0], new_ext_network))
print (arreglo_maestro)