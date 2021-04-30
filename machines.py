import requests
import asyncio
import aiohttp

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
### Usamos aiohttp en vez de requests
async def vm_stop(session, headers,URL,customer_id,cloudspace_id,vm_id,force):
    data = {
        'force': "%s" %(force)
    }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s/stop' % (customer_id, cloudspace_id, vm_id)
    #print(api_get, data)
    #vm_stopped =requests.post(URL + api_get, headers=headers, params=data)

    async with session.post(URL + api_get, headers=headers, params=data) as resp:
        vm_stopped = await resp.json()

    if resp.status == requests.codes.ok:
        print("VM_id:%s detenida exitosamente"%(vm_id))
    else:
        print("Advertencia vm_id: %s no se pudo detener. Mensaje: %s \n api_get %s\n data:"
          %(vm_id,vm_stopped,api_get),data)
    return (resp)

async def async_vm_get(session, headers,URL,customer_id,cloudspace_id,vm_id):
    data = {
            }
    #print(f'API GET-->{vm_id}<---')
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s' % (customer_id, cloudspace_id, vm_id)
    async with session.get(URL + api_get, headers=headers) as resp:
        vm_goted = await resp.json()
    if resp.status == requests.codes.ok:
        print("Se obtuvo la infor de VM_id:%s exitosamente\n"%(vm_id),vm_goted)
    else:
        print("Advertencia vm_id: %s no se pudo detener información. Mensaje: %s \n api_get %s\n data:"
          %(vm_id,vm_goted,api_get),resp)
    return (resp)

def vm_get( headers,URL,customer_id,cloudspace_id,vm_id):
    data = {
            }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s' % (customer_id, cloudspace_id, vm_id)
    print(f'API GET-->{ URL+ api_get}<---')
#    https: // cloud.amx.gig.tech / api / 1 / customers / exfo_1 / cloudspaces / dXMtamFjLWRjMDEtMDAyOjEzMDI / vms / 3338
    resp =  requests.get(URL + api_get, headers=headers)
    vm_goted = resp.json()

    if resp.status_code == requests.codes.ok:
        print("Se obtuvo la infor de VM_id:%s exitosamente\n"%(vm_id),vm_goted)
    else:
        print("Advertencia vm_id: %s no se pudo detener información. Mensaje: %s \n api_get %s\n data:"
          %(vm_id,vm_goted,api_get),resp)
    return (resp)
async def vm_delete(session,headers,URL,customer_id,cloudspace_id,vm_id,force):
    data = {
        'permanently': "%s" %(force)
    }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s' % (customer_id, cloudspace_id, vm_id)
    #print(api_get, data)
    async with session.delete(URL + api_get, headers=headers, params=data) as resp:
        vm_deleted = await resp.json()
    if resp.status == requests.codes.ok:
        print("VM_id:%s borrada exitosamente"%(vm_id))
    else:
        print("--->vm_id: %s no se pudo borrar. Mensaje: %s \n api_get %s\n data:"
              %(vm_id,vm_deleted,api_get),data)
    return (resp)

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
              % (cloudspace_id, vms_listed.json(), api_get), data)
    return (vms_list)

async def vm_create(session, headers,URL,customer_id,cloudspace_id,data):
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms' % (customer_id, cloudspace_id)
    async with  session.post(URL + api_get, headers=headers, params=data) as resp:
        await resp.json()
    if resp.status_code == requests.codes.ok:
        print(f'VM creada:{data["name"]} correctamente')
    else:
        print("creación vm %s fallo por:%s" % (data["name"],resp.text))
    return (resp)


async def attach_external_nics_to_vm(session, headers,URL,customer_id,cloudspace_id,vm_id,
                               external_network_id,external_network_ip):
    data = {
        'external_network_id': "%s" % (external_network_id),
        'external_network_ip': "%s" % (external_network_ip)
    }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s/external-nics' % (customer_id, cloudspace_id, vm_id)
    async with session.post(URL + api_get, headers=headers, params=data) as resp:
        network_attached = await resp.json()
        if resp.status == requests.codes.ok:
            print("External_network_id:%s conectada a vm_id:%s"%(external_network_id,vm_id))
        else:
            print("ADVERTENCIA: Conexion a External_network_Id: %s de vm_id:%s fallo. Mensaje: %s \n api_get %s\ndata:"
                  %(external_network_id,vm_id,success.text,api_get),data)
        return (resp)

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