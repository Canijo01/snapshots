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