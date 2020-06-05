import requests


class EntandoClient(object):

    def __init__(self, url, access_token):
        self._url = url
        self._headers = {'authorization': 'Bearer ' + access_token}

    def update_widget(self, widget):
        r = requests.put(self._url + "/api/widgets/" + widget["code"],
                         json=widget, headers=self._headers)
        if r.status_code == 404:
            requests.post(self._url + "/api/widgets", json=widget,
                          headers=self._headers)
