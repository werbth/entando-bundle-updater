import logging
import os
from pathlib import Path

import requests


class EntandoClient:

    def __init__(self, url, access_token):
        self._url = url
        self._headers = {'authorization': 'Bearer ' + access_token}

    def update_widget(self, widget):
        r = requests.put(self._url + "/api/widgets/" + widget["code"],
                         json=widget, headers=self._headers)
        if r.status_code == 404:
            r = requests.post(self._url + "/api/widgets", json=widget,
                              headers=self._headers)
        logging.info("Loading Widget {}: {}".format(widget["code"],
                                                    r.status_code))

    def update_fragment(self, fragment):
        r = requests.put(self._url + "/api/fragments/" + fragment["code"],
                         json=fragment, headers=self._headers)
        if r.status_code == 404:
            r = requests.post(self._url + "/api/fragments", json=fragment,
                              headers=self._headers)
        logging.info("Loading fragment {}: {}".format(fragment["code"],
                                                      r.status_code))

    def update_page_model(self, page_model):
        r = requests.put(self._url + "/api/pageModels/" + page_model["code"],
                         json=page_model, headers=self._headers)
        if r.status_code == 404:
            r = requests.post(self._url + "/api/pageModels", json=page_model,
                              headers=self._headers)
        logging.info("Loading page model {}: {}".format(page_model["code"],
                                                        r.status_code))

    def upload_resource(self, resource):
        payload = {'protectedFolder': False, 'currentPath': resource['path']}
        r = requests.get(self._url + "/api/fileBrowser/file", params=payload,
                         headers=self._headers)
        if r.status_code == 404:
            r = requests.post(self._url + "/api/fileBrowser/file",
                              json=resource,
                              headers=self._headers)
        else:
            r = requests.put(self._url + "/api/fileBrowser/file", json=resource,
                             headers=self._headers)
        logging.info("Uploading resource {}: {}".format(resource["path"],
                                                        r.status_code))

    def create_directory(self, directory_name):
        path = Path(directory_name)
        current_name = ""
        for d in path.parts:
            current_name = os.path.join(current_name, d)
            directory = {
                'protectedFolder': False,
                'path': '/' + current_name
            }
            r = requests.post(self._url + "/api/fileBrowser/directory",
                              json=directory, headers=self._headers)
            logging.info(
                "Creating directory {}: {}".format('/' + current_name,
                                                   r.status_code))
