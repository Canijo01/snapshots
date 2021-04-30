import aiohttp
import asyncio
import time
import configparser
import requests

from  obtentoken import *

config = configparser.ConfigParser()
a = config.read("config.ini")

CUSTOMER_ID = config.get("AMX", "CUSTOMER_ID")
CLOUDSPACE_ID = config.get("AMX", "CLOUDSPACE_ID")
LOCATION = config.get("AMX", "LOCATION")
TOKEN = config.get("AMX", "TOKEN")
URL = config.get("AMX", "URL")
start_time = time.time()
jH = get_headers_js(TOKEN)

data = {}
api_get = f'api/1/customers/{CUSTOMER_ID}/cloudspaces/{CLOUDSPACE_ID}/vms'
#    cloudspace = requests.get(URL + api_get, headers=jH, params=data)

def cloudspace_vms_get(headers, URL, customer_id,cloudspace_id):
    data = {
            }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms' % (customer_id,cloudspace_id)
    cloudspace = requests.get(URL + api_get, headers=headers, params=data)
    if cloudspace.status_code == requests.codes.ok:
        print("Se obtuvieron las vms para cloudspace_id:%s"%(cloudspace_id))
    else:
        print("ERROR: NO se obtuvieron las vms para cloudspace_Id: %s. Mensaje: %s \n\t api_get %s\n\tdata:"
              %(cloudspace_id,cloudspace.text,api_get),data)
    return (cloudspace)

async def vm_stop(session, headers,URL,customer_id,cloudspace_id,vm_id,force):
    data = {
        'force': "%s" %(force)
    }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s/stop' % (customer_id, cloudspace_id, vm_id)
    async with session.post(URL + api_get, headers=headers, params=data) as resp:
        vm_stopped = await resp.json()
    if resp.status == requests.codes.ok:
        print("VM_id:%s detenida exitosamente" % (vm_id))
    else:
        print("Advertencia vm_id: %s no se pudo detener. Mensaje: %s \n api_get %s\n data:"
              % (vm_id, vm_stopped.text, api_get), data)
    return(resp)

async def stop_vms_cloudspace(headers, URL,customer_id,cloudspace_id,force):
    ids = []
    vms = cloudspace_vms_get(headers, URL, customer_id,cloudspace_id)
    if vms.status_code == requests.codes.ok:
        async with aiohttp.ClientSession() as session:
            tasks = []
            my_vms = vms.json()
            if (my_vms["result"]):
                for vm in my_vms["result"]:
                    tasks.append(asyncio.ensure_future(vm_stop(session,headers, URL, customer_id,cloudspace_id,vm["vm_id"],force)))
                results = await asyncio.gather(*tasks)
                return(results)
            else:
                print("No hay vms a detener en cloudspace_id:%s"%(cloudspace_id))
    else:
        print("No se pudo obtener lista de vms para cloudspace_id: %s Mensaje:%s \n"%(cloudspace_id,vms.text))
    return(ids)
async def get_pokemon(session,url):
    async with session.get(URL + api_get, headers=jH, params=data) as resp:
    #async with requests.get(url) as resp:
        pokemon = await resp.json()
        return pokemon['result']
asyncio.run(stop_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True))
#stop_vms_cloudspace(jH,URL,CUSTOMER_ID,CLOUDSPACE_ID,True)

print("--- %s seconds ---" % (time.time() - start_time))