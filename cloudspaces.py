import requests
from machines import *
def cloudspaceslist(headers,URL):
    data = {
        'includedeleted': "%s" % (True)
    }
    api_get = 'restmachine/cloudapi/cloudspaces/list'
    cloudspace = requests.post(URL + api_get, headers=headers, data=data)
    return (cloudspace)


def cloudspaceget(headers, URL, cloudspaceId):
    data = {
                'cloudspaceId': "%s" % (cloudspaceId)
            }
    api_get = 'restmachine/cloudapi/cloudspaces/get'
    cloudspace = requests.post(URL + api_get, headers=headers, data=data)
    return (cloudspace)



#####
##
##  New API
##
#####

def cloudspaceslist2(headers,URL,customer_id):
    data = {
        'include_deleted': True,
        'location': ""
    }
    api_get = 'api/1/customers/%s/cloudspaces' % (customer_id)
    cloudspace = requests.get(URL + api_get, headers=headers, params=data)
    if cloudspace.status_code == requests.codes.ok:
        print("Se obtuvieron los cloudspaces para customer_id:%s"%(customer_id))
    else:
        print("ERROR: NO se obtuvieron los cloudspaces para Customer_Id: %s. Mensaje %s: %s \n\t api_get %s\n\tdata:"
              %(customer_id,cloudspace.text,api_get),data)
    return (cloudspace)

def cloudspace_vms_get(headers, URL, customer_id,cloudspace_id):
    data = {
            }
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms' % (customer_id,cloudspace_id)
    cloudspace = requests.get(URL + api_get, headers=headers, params=data)
    if cloudspace.status_code == requests.codes.ok:
        print("Se obtuvieron las vms para cloudspace_id:%s"%(cloudspace_id))
    else:
        print("ERROR: NO se obtuvieron las vms para cloudspace_Id: %s. Mensaje %s: %s \n\t api_get %s\n\tdata:"
              %(cloudspace_id,cloudspace.text,api_get),data)
    return (cloudspace)

def stop_vms_cloudspaces(headers, URL,customer_id,force):
    ids = []
    cloudspaces = cloudspaceslist2(headers, URL,customer_id)

    if cloudspaces.status_code == requests.codes.ok:
        my_cloudspaces = cloudspaces.json()

        for i in my_cloudspaces["result"]:
            print("cloudspaceId: %s, location: %s, status:%s, name: %s" % (
            i["cloudspace_id"], i["location"], i["status"], i["name"]))
            vms = cloudspace_vms_get(headers, URL, customer_id,i["cloudspace_id"])
            if vms.status_code == requests.codes.ok:
                my_vms = vms.json()
                for vm in my_vms["result"]:
                    stops=vm_stop(headers, URL, customer_id,i["cloudspace_id"],vm["vm_id"], force)
                    #print("vm_Id: %s, name:%s, stop status:%s" % (m["vm_id"], m["name"],stops))
                    ids.append([v["vm_id"],stops])
    else: print("No se obtuvieron los cloudspaces de customer_id:%s mensaje:%s"%(customer_id,cloudspaces.text))
    return(ids)
def stop_vms_cloudspace(headers, URL,customer_id,cloudspace_id,force):
    ids = []
    vms = cloudspace_vms_get(headers, URL, customer_id,cloudspace_id)
    if vms.status_code == requests.codes.ok:
        my_vms = vms.json()
        if (my_vms["result"]):
            for vm in my_vms["result"]:
                stops=vm_stop(headers, URL, customer_id,cloudspace_id,vm["vm_id"],force)
                #print("vm_Id: %s, name:%s, stop status:%s" % (m["vm_id"], m["name"],stops))
                ids.append([vm["vm_id"],stops])
        else:
            print("No hay vms a detener en cloudspace_id:%s"%(cloudspace_id))
    else:
        print("No se pudo obtener lista de vms para cloudspace_id: %s Mensaje:%s \n"%(cloudspace_id,vms.text))
    return(ids)
def delete_vms_cloudspace(headers, URL,customer_id,cloudspace_id,force):
    ids = []
    machines = cloudspace_vms_get(headers, URL, customer_id,cloudspace_id)
    if machines.status_code == requests.codes.ok:
        my_machines = machines.json()
        for m in my_machines["result"]:
            stops=machine_delete(headers, URL, customer_id,cloudspace_id,m["vm_id"],force)
            #print("vm_Id: %s, name:%s, delete status:%s" % (m["vm_id"], m["name"],stops))
            #ids.append([m["vm_id"],stops])
    else: print(cloudspaces.status_code)
    return(ids)


def get_consumption_cloudspace(headers, URL,customer_id,cloudspace_id,start,end):
    data = {
        'end': "%s" %(end),
        'start': "%s" %(start)
    }
    print("Obteniendo consumo de cloudspace_id: %s" %(cloudspace_id))
    api_get = 'api/1/customers/%s/cloudspaces/%s/consumption' % (customer_id,cloudspace_id)
    consumption = requests.get(URL + api_get, headers=headers, params=data)
    if consumption.status_code == requests.codes.ok:
        print("Se obtuvieron la informacion de consumo del cloudspaceId :%s" % (cloudspace_id))
    else:
        print("ERROR: NO se obtuvieron los datos de consumo del cloudspaceId: %s. Mensaje %s: \n\t api_get %s\n\tdata:"
              % (cloudspace_id, consumption.text, api_get), data)
    return (consumption)

def stop_vms_cloudspaces(headers, URL,customer_id,force):
    ids = []
    cloudspaces = cloudspaceslist2(headers, URL,customer_id)

    if cloudspaces.status_code == requests.codes.ok:
        my_cloudspaces = cloudspaces.json()

        for i in my_cloudspaces["result"]:
            print("cloudspaceId: %s, location: %s, status:%s, name: %s" % (
            i["cloudspace_id"], i["location"], i["status"], i["name"]))
            vms = cloudspace_vms_get(headers, URL, customer_id,i["cloudspace_id"])
            if vms.status_code == requests.codes.ok:
                my_vms = vms.json()
                for vm in my_vms["result"]:
                    stops=vm_stop(headers, URL, customer_id,i["cloudspace_id"],vm["vm_id"], force)
                    #print("vm_Id: %s, name:%s, stop status:%s" % (m["vm_id"], m["name"],stops))
                    ids.append([v["vm_id"],stops])
    else: print("No se obtuvieron los cloudspaces de customer_id:%s mensaje:%s"%(customer_id,cloudspaces.text))
    return(ids)
