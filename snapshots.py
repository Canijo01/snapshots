import time
from cloudspaces import *
from machines import *

def snapshotcloudspaces(headers, URL):
    ids = []
    start = int(round(time.time()))
    snapname = "mSnap%s" % (start)
    cloudspaces = cloudspaceslist(headers, URL)
    if cloudspaces.status_code == requests.codes.ok:
        my_cloudspaces = cloudspaces.json()
        for i in my_cloudspaces:
            print("cloudspaceId: %s, accountId: %s, status:%s, name: %s" % (
            i["id"], i["accountId"], i["status"], i["name"]))
            cloudspace = cloudspaceget(headers, URL, ["id"])
            if cloudspace.status_code == requests.codes.ok:
                my_cloudspaces = cloudspace.json()
                print(my_cloudspaces)
            machines = machinelist(headers, URL, i["id"])
            if machines.status_code == requests.codes.ok:
                my_machines = machines.json()
                for m in my_machines:
                    snaps=machinesnapshot(headers, URL, m["id"], snapname, True)
                    print("machineId: %s, machineName:%s, snapshot status:%s" % (m["id"], m["name"],snaps))
                    ids.append([m["id"],snaps])

    return(ids)

def stopmachinescloudspaces(headers, URL,cloudspaces):
    ids = []
    for i in cloudspaces:
        machines = machinelist(headers, URL, i)
        if machines.status_code == requests.codes.ok:
            my_machines = machines.json()
            for m in my_machines:
                stop = machinesstop(headers, URL, m["id"], False)
                print("machineId: %s, machineName:%s, status:%s" % (m["id"], m["name"],stop))
                ids.append([m["id"],stop])

    return(ids)


#########
##
##  New API
##
#########
def snapshotcloudspaces2(headers, URL,customer_id):
    ids = []
    start = int(round(time.time()))
    snapname = "mSnap%s" % (start)
    cloudspaces = cloudspaceslist2(headers, URL,customer_id)

    if cloudspaces.status_code == requests.codes.ok:
        my_cloudspaces = cloudspaces.json()
        #print(my_cloudspaces)
        for i in my_cloudspaces["result"]:
            #print("cloudspaceId: %s, location: %s, status:%s, name: %s" % (
            #i["cloudspace_id"], i["location"], i["status"], i["name"]))
            machines = cloudspace_vms_get(headers, URL, customer_id,i["cloudspace_id"])
            if machines.status_code == requests.codes.ok:
                my_machines = machines.json()
                for m in my_machines["result"]:
                    snaps=disk_snapshot(headers, URL, customer_id,i["location"],m["disks"][0], snapname, True)
                    #print("vm_Id: %s, name:%s, snapshot status:%s" % (m["vm_id"], m["name"],snaps))
                    ids.append([m["vm_id"],snaps])
    else: print(cloudspaces.status_code,"-->",cloudspaces.text)
    return(ids)


def clone_machine_in_cloudspace(headers, URL,customer_id,cloudspace_id,location):
    ids = []
    start = int(round(time.time()))
    snapname = "mSnapClone%s" % (start)
    machines = cloudspace_vms_get(headers, URL, customer_id,cloudspace_id)
    if machines.status_code == requests.codes.ok:
        my_machines = machines.json()
        for m in my_machines["result"]:
            snaps=disk_snapshot(headers, URL, customer_id,location,m["disks"][0], snapname, True)
            if snaps.status_code == requests.codes.ok:
                snap_id= disk_get_snapshot_id(headers,URL,customer_id,location,m["disks"][0],snapname)
                #print("vm_Id: %s, name:%s, snap_id:%s" % (m["vm_id"], m["name"],snap_id))
                print("Intentando clonar disk_id:%s"%(m["disks"][0]))
                clones = disk_clone(headers,URL,customer_id,location,m["disks"][0],snap_id,m["name"],m["name"],True)
                if clones.status_code == requests.codes.ok:
                    my_clones = clones.json()
                    for c in my_clones["result"]:
                        ids.append([c])
                else:
                    print("ERROR: Disk_clone para disk_id %s fallo, mensaje:%s"%(m["disks"][0],clones.text))
            else:
                print("ERROR: Instantea de disk_id: %s fallo. Mensaje:%s"%(m["disks"][0],snaps.text))
        print(ids)
    else: print(machines.status_code)

    return(ids)
def disk_snapshot(headers,URL,customer_id,location,disk_id,name,all_vm_disks):
    data = {
        'snapshot_name': "%s" % (name),
        'all_vm_disks': all_vm_disks
    }
    api_get = 'api/1/customers/%s/locations/%s/disks/%s/snapshots'%(customer_id,location,disk_id)
    #print(api_get,data)
    snapshot = requests.post(URL + api_get, headers=headers, params=data)
    if snapshot.status_code == requests.codes.ok:
        print("Instantanea de disk_id:%s creada exitosamente"%(disk_id))
    else:
        print("Error. Instantanea de disk_id %s fallo. Mensaje %s \n api_get %s\ndata:"
              %(disk_id,snapshot.text,api_get),data)
    return (snapshot)

def disk_get_snapshots(headers,URL,customer_id,location,disk_id):
    data = {
        }
    api_get = 'api/1/customers/%s/locations/%s/disks/%s/snapshots'%(customer_id,location,disk_id)
    #print(api_get,data)

    snapshot = requests.get(URL + api_get, headers=headers, params=data)
    if snapshot.status_code == requests.codes.ok:
        print ("La lista de instantaneas del disk_id:%s fue recuperada exitosamente"%(disk_id))
    else:
        print("ERROR: La lista de instantaneas de disk_id: %s fallo, mensaje:%s \n api_get %s\n data:"
              %(disk_id,snapshot.text,api_get),data)
    return (snapshot)

def disk_delete_snapshot(headers,URL,customer_id,location,disk_id,snapshot_id):
    data = {
        }
    api_get = 'api/1/customers/%s/locations/%s/disks/%s/snapshots/%s'%(customer_id,location,disk_id,snapshot_id)
    #print(api_get,data)
    snapshot = requests.delete(URL + api_get, headers=headers, params=data)
    if snapshot.status_code == requests.codes.ok:
        print ("Borrado de instantanea de disk_id:%s fue exitoso"%(disk_id))
    else:
        print("ADVERTENCIA: Borrado de instantanea de disk_id %s fallo, snapshot_id %s \n\tMensaje:%s"
              %(disk_id,snapshot_id,snapshot.text))

    return (snapshot)

def disk_get_snapshot_id(headers,URL,customer_id,location,disk_id,snapshot_name):
    snapshot_id=""
    #obtener lista de snapshots disponibles
    snapshots = disk_get_snapshots(headers,URL,customer_id,location,disk_id)
    if snapshots.status_code == requests.codes.ok:
        my_snaps = snapshots.json()
        #encontrar el snashot_id que corresponda al nombre de la instantanea
        for m in my_snaps["result"]:
            if ( m["snapshot_name"] == snapshot_name):
                snapshot_id = m["snapshot_id"]
    else:
        print("Error no se obtuvo el id de la instantanea:%s para disk_id:%s"%(snapshot_name,disk_id))
    return (snapshot_id)

def disk_clone(headers,URL,customer_id,location,disk_id,snapshot_id,name,description,all_vm_disks):
    data = {
        'name': "%s" % (name),
        'description': "%s" % (description),
        'all_vm_disks': all_vm_disks
    }
    api_get = 'api/1/customers/%s/locations/%s/disks/%s/snapshots/%s/clone'\
              %(customer_id,location,disk_id,snapshot_id)
    #print(api_get,data)
    snapshot = requests.post(URL + api_get, headers=headers, params=data)
    if snapshot.status_code != requests.codes.ok:
        print("ERROR: Fallo clone de disk_id:%s mensaje:%s \n Api get: %s\n data:"
              %(disk_id,snapshot.text,api_get),data)
    return (snapshot)

def clone_machine_from_disk_id(headers, URL,customer_id,cloudspace_id,location,data):
    ids = []
    vm=""
    start = int(round(time.time()))
    snapname = "mSnapClone%s" % (start)
    if (data["snapshot_id"]):
        snapname=data["snapshot_name"]
        snap_id=data["snapshot_id"]
    else:
        snaps=disk_snapshot(headers, URL, customer_id,location,data["disk_id"], snapname, data["all_vm_disks"])
        if snaps.status_code == requests.codes.ok:
            snap_id = disk_get_snapshot_id(headers, URL, customer_id, location, data["disk_id"], snapname)
    if snap_id:
        print("Iniciando clonado de instantanea: %s snapid: %s"%(snapname,snap_id))
        clones = disk_clone(
            headers,
            URL,
            customer_id,
            location,
            data["disk_id"],
            snap_id,
            data["disk_name"],
            data["disk_description"],
            data["all_vm_disks"])
        ##Intentar borrar el snapshot que se creo para el clonado. Se quito ya que no lo puede hacer el G8
        #disk_delete_snapshot(headers,URL,customer_id,location,data["disk_id"],snap_id)
        if clones.status_code == requests.codes.ok:
            my_clones = clones.json()
            for c in my_clones["result"]:
                ids.append([c])
            #print(ids)
            for d in ids:
                #print(d,d[0])
                boot_disk_id=d[0]["new_disk_id"]
            vm_data = {
                'name': "%s" % (data["name"]),
                'description': "%s" % (data["description"]),
                'vcpus': "%s" % (data["vcpus"]),
                'memory': "%s" %(data["memory"]),
                'private_ip': "%s" % (data["private_ip"]),
                'boot_disk_id': "%s" % (boot_disk_id),
                'os_type': "%s" % (data["os_type"]),
                'os_name': "%s" % (data["os_name"]),
                'data_disks': data["data_disks"]
            }
            print("Inicando creación de vm: %s desde disco: %s"%(vm_data["name"],vm_data["boot_disk_id"]))
            ## Se crea la vm usando el disco clonado que tiene el boot_disk_id
            vm=vm_create(headers, URL, customer_id, cloudspace_id, vm_data)
            if vm.status_code == requests.codes.ok:
                my_vms = vm.json()
                vm_id= my_vms["vm_id"]
                print("La vm : %s tiene un vm_id: %s"%(data["name"],vm_id))
                #Una ves creada la VM se le anexan los las redes externas

                for external_network_id in data["externalnetworks"]:
                    attach_external_nics_to_vm(
                                   headers, URL, customer_id, cloudspace_id,vm_id, external_network_id,"")

                ### Aqui faltaria anexar discos adicionales en un futuro. En caso de que la vm de origen tuviera varios
                ### discos.
            else:
                print("creación vm %s fallo por:%s"%(data["name"],vm.text))

            #print("disk_id: %s, name:%s, snap_id:%s" % (data["disk_id"], data["disk_name"], snap_id))
            #print(vm.text)
        #print(ids)
    else: print("ERROR: No se logro la instantanea %s --> %s"%(snaps.status_code,snaps.text))

    return(vm)

async def deploy_vm_from_image_id(session,headers, URL,customer_id,cloudspace_id,data):
    vm_data = data[0]
    print("Inicando creación de vm: %s desde image_id: %s"%(vm_data["name"],vm_data["image_id"]))
    ## Se crea la vm usando el disco clonado que tiene el boot_disk_id
    api_get = 'api/1/customers/%s/cloudspaces/%s/vms' % (customer_id, cloudspace_id)
    #async with  session.post(URL + api_get, headers=headers, params=vm_data) as resp:
    #    vm = await resp.json()
    resp = await session.post(URL + api_get, headers=headers, params=vm_data,timeout=None)
    vm = await resp.json()
    if resp.status == requests.codes.ok:
        vm_id=vm["vm_id"]
        print(f'VM creada:{vm_data["name"]} correctamente ID:{vm_id}')
        if data[1] :
            tasks = []
            for e_network in data[1]:
                data = {
                    'external_network_id': "%s" % (e_network[0]),
                    'external_network_ip': "%s" % (e_network[1])
                }
                api_get = 'api/1/customers/%s/cloudspaces/%s/vms/%s/external-nics' % (customer_id, cloudspace_id, vm_id)
             #   tasks.append(asyncio.ensure_future(session.post(URL + api_get, headers=headers, params=data)))

            #    async with session.post(URL + api_get, headers=headers, params=data) as resp:
            #       network_attached = await resp.json()
                resp2 = await session.post(URL + api_get, headers=headers, params=data,timeout=None)
                success = await resp2.json()
            #results = await asyncio.gather(*tasks)
            #for resp in results:
                #print(resp)
                if resp2.status == requests.codes.ok:
                    print("External_network_id:%s conectada a vm_id:%s" % (e_network[0], vm_id))
                else:
                    print(
                        "ADVERTENCIA: Conexion a External_network_Id: %s de vm_id:%s fallo. Mensaje: %s \n api_get %s\ndata:"
                        % (e_network[0], vm_id, e_network[1], api_get), data)
    else:
        print("creación vm %s fallo por:%s" % (vm_data["name"], resp.text))
    return (resp)


