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
