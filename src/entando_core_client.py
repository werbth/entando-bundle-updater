import logging
import os
from pathlib import Path

import requests


class EntandoClient:

    def __init__(self, url, access_token):
        self._url = url
        self._headers = {'authorization': 'Bearer ' + access_token}

    def update_widget(self, widget):
        logging.info("Loading Widget {}".format(widget["code"]))
        r = requests.put(self._url + "/api/widgets/" + widget["code"],
                         json=widget, headers=self._headers)
        if r.status_code == 404:
            requests.post(self._url + "/api/widgets", json=widget,
                          headers=self._headers)

    def upload_resource(self, resource):
        logging.info("Uploading resource {}".format(resource["path"]))
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
        logging.info(
            "Result for {}: {}".format(resource["path"], r.status_code))

    def create_directory(self, directory_name):
        path = Path(directory_name)
        current_name = ""
        for d in path.parts:
            current_name = os.path.join(current_name, d)
            directory = {
                'protectedFolder': False,
                'path': '/' + current_name
            }
            logging.info(
                "Creating directory {} on Entando".format('/' + current_name))
            r = requests.post(self._url + "/api/fileBrowser/directory",
                              json=directory, headers=self._headers)
            logging.info("Result for directory {}: {}".format(current_name,
                                                              r.status_code))
