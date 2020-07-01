import requests

def get_token(APP_ID, SECRET, IYO_URL):
    """
    :return: Regresa los headers para poder hacer las llamadas a las apis de GIG
    Utiliza las variables de IYO_URL, APP_ID y SECRET
    """

    data = {
        'grant_type': 'client_credentials',
        'client_id': APP_ID,
        'client_secret': SECRET,
        'response_type': 'id_token'
    }
    iyo_token = requests.post(IYO_URL, data=data)

    headers = {
        'Accept': 'application/json',
        'Authorization': "bearer {0}".format(iyo_token.text)
    }

    if iyo_token.status_code == requests.codes.ok:
        myheaders = {
            'Accept': 'application/json',
            'Authorization': "bearer %s" % (iyo_token.text),
        }
    else:
        print("no se obtuvieron el token de acceso")
        myheaders = {
            'Accept': 'application/json',

            'Authorization': "bearer %s" % (iyo_token.text)
        }
    return iyo_token.text


def get_headers_js(token):
    myheaders = {
        'Accept': 'application/json',
        'Authorization': "bearer %s" % (token),
    }
    return myheaders


def get_headers_os(token):
    myheaders = {
        'Accept': 'application/octet-stream',
        'Authorization': "bearer %s" % (token),
    }
    return myheaders


