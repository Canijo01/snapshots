import requests

def machinelist(headers,URL,cloudspaceId):
    data = {
        'cloudspaceId': "%s" % (cloudspaceId)
    }
    api_get = 'restmachine/cloudapi/machines/list'
    machinelist = requests.post(URL + api_get, headers=headers, data=data)
    return (machinelist)

def machinesnapshot(headers,URL,machineId,name,force):
    data = {
        'machineId': "%s" % (machineId),
        'name': "%s" % (name),
        'force': "%s" % (force)
    }
    api_get = 'restmachine/cloudapi/machines/snapshot'
    snapshot = requests.post(URL + api_get, headers=headers, data=data)
    return (snapshot)
def machinesstop(headers,URL,machineId,force):
    data = {
        'machineId': "%s" % (machineId),
        'force': "%s" % (force)
    }
    api_get = 'restmachine/cloudapi/machines/stop'
    snapshot = requests.post(URL + api_get, headers=headers, data=data)
    return (snapshot)
def machines_stop(headers,URL,vm_id,force):
    data = {
        'permanently': True
    }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s/snapshots' % (customer_id, cloudspace_id, vm_id)
    print(api_get, data)
    machine_delted = requests.post(URL + api_get, headers=headers, params=data)
    return (machine_delted)


###
### New API
###

def vm_stop(headers,URL,customer_id,cloudspace_id,vm_id,force):
    data = {
        'force': "%s" %(force)
    }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s/stop' % (customer_id, cloudspace_id, vm_id)
    #print(api_get, data)
    vm_stopped = requests.post(URL + api_get, headers=headers, params=data)
    if vm_stopped.status_code == requests.codes.ok:
        print("VM_id:%s detenida exitosamente"%(vm_id))
    else:
        print("Advertencia vm_id: %s no se pudo detener. Mensaje: %s \n api_get %s\n data:"
              %(vm_id,vm_stopped.text,api_get),data)

    return (vm_stopped)
def machine_delete(headers,URL,customer_id,cloudspace_id,vm_id,force):
    data = {
        'permanently': "%s" %(force)
    }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s' % (customer_id, cloudspace_id, vm_id)
    #print(api_get, data)
    vm_deleted = requests.delete(URL + api_get, headers=headers, params=data)
    if vm_deleted.status_code == requests.codes.ok:
        print("VM_id:%s borrada exitosamente"%(vm_id))
    else:
        print("--->vm_id: %s no se pudo borrar. Mensaje: %s \n api_get %s\n data:"
              %(vm_id,vm_deleted.text,api_get),data)

    return (vm_deleted)
def machine_list(headers,URL,customer_id,cloudspace_id):
    data = {
        'force': "%s" %(force)
    }

    api_get = 'api/1/customers/%s/cloudspaces/%s/vms' % (customer_id, cloudspace_id)
    print(api_get, data)
    vms_listed = requests.post(URL + api_get, headers=headers, params=data)
    if vm_listed.status_code == requests.codes.ok:
        print("Lista de vms para cloudspace_id:%s obtenida exitosamente" % (cloudspace_id))
    else:
        print("--->No se pudo obtener lista de vms para cloudspace_id: %s. Mensaje %s : %s \n api_get %s\n data:"
              % (cloudspace_id, vms_listed.text, api_get), data)
    return (vms_list)
#Model
#{
#    "result": [
#        {
#            "vm_id": 0,
#            "name": "string",
#            "status": "string",
#            "stack_id": 0,
#            "creation_time": 0,
#            "update_time": 0,
#            "reference_id": "string",
#            "image_id": 0,
#            "storage": 0,
#            "vcpus": 0,
#            "memory": 0,
#            "appliance": true,
#            "disks": [
#                0
#            ],
#            "network_interfaces": [
#                {
#                    "device_name": "string",
#                    "mac_address": "string",
#                    "ip_address": "string",
#                    "network_id": 0
#                }
#            ]
#        }
#    ]
#}
def vm_create(headers,URL,customer_id,cloudspace_id,data):
    #data = {
    #    'name': "%s" % (name),
    #    'description': "%s" % (description),
    #    'disk_size': "%s" % (disk_size),
    #    'data_disks': "%s" % (data_disks)
    #    'vcpus': "%s" % (vcpus),
    ##    'memory': "%s" %(memory),
    #    'private_ip': "%s" % (private_ip),
    #    'image_id': "%s" % (image_id),
    #    'os_type': "%s" % (os_type)
    #}

    api_get = 'api/1/customers/%s/cloudspaces/%s/vms' % (customer_id, cloudspace_id)
    #print(api_get, data)
    vm_created = requests.post(URL + api_get, headers=headers, params=data)
    if vm_created.status_code == requests.codes.ok:
        print("VM creadas:%s correctamente"%(data["name"]))
    else:
        print("--->Creacion de VM fallo. Mensaje %s fallo: %s \n api_get %s\ndata:"
              %(data["name"],vm_created.text,api_get),data)
    return (vm_created)


def attach_external_nics_to_vm(headers,URL,customer_id,cloudspace_id,vm_id,
                               external_network_id,external_network_ip):
    data = {
        'external_network_id': "%s" % (external_network_id),
        'external_network_ip': "%s" % (external_network_ip)
    }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s/external-nics' % (customer_id, cloudspace_id, vm_id)
    success = requests.post(URL + api_get, headers=headers, params=data)
    if success.status_code == requests.codes.ok:
        print("External_network_id:%s conectada a vm_id:%s"%(external_network_id,vm_id))
    else:
        print("ADVERTENCIA: Conexion a External_network_Id: %s de vm_id:%s fallo. Mensaje: %s \n api_get %s\ndata:"
              %(external_network_id,vm_id,success.text,api_get),data)
    return (success)

def vm_export_s3(headers,URL,customer_id,cloudspace_id,vm_id,
                               data):
    ## En data se requiere
    ## link: http del servidor s3
    ## key:
    ##secret:
    ##region: normalmente us-east-1
    ##bucket:
    ##object_name: normbre del archivo a exportar en formato ova
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s/export-s3' % (customer_id, cloudspace_id, vm_id)
    print("Intentando exportar vm_id: %s a  %s/%s"%(vm_id,data["bucket"],data["object_name"]))
    success = requests.post(URL + api_get, headers=headers, params=data)
    if success.status_code == requests.codes.ok:
        print("vm_id:%s exportada exitosamente a objeto:%s"%(vm_id,data["object_name"]))
    else:
        print("ADVERTENCIA: La vm_id: %s no se pudo exportar. Mensaje: %s \n api_get %s\ndata:"
              %(vm_id,success.text,api_get),data)
    return (success)
def vm_import_s3(headers,URL,customer_id,cloudspace_id,vm_id,
                               data):
    ## En data se requiere
    ## link: http del servidor s3
    ## key:
    ##secret:
    ##region: normalmente us-east-1
    ##bucket:
    ##object_name: normbre del archivo a exportar en formato ova
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/import-s3' % (customer_id, cloudspace_id)
    print("Intentando importar name: %s de  %s/%s"%(data["name"],data["bucket"],data["object_name"]))
    success = requests.post(URL + api_get, headers=headers, params=data)
    if success.status_code == requests.codes.ok:
        vm_id = success.json()["vm_id"]
        print("vm_id:%simportada exitosamente de %s/%s"%(vm_id,data["bucket"],data["object_name"]))
    else:
        print("ADVERTENCIA: La VM: %s no se pudo importar. Mensaje: %s \n api_get %s\ndata:"
              %(data["name"],success.text,api_get),data)
    return (success)