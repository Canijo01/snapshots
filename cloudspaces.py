import requests

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



