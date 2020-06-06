import logging

import yaml

from entando_core_client import EntandoClient


class Loader:

    def __init__(self, url, access_token):
        self._client = EntandoClient(url, access_token)

    def load(self, bundle_directory):
        logging.info("Start processing main descriptor")
        with (bundle_directory / "descriptor.yaml").open('r') as descriptor:
            descriptor_yaml = yaml.load(descriptor, Loader=yaml.FullLoader)

            # load widgets
            widgets = descriptor_yaml['components']['widgets']
            self._load_widgets(bundle_directory, widgets)

    def _load_widgets(self, bundle_directory, widgets):
        logging.info("Loading widgets")
        for w in widgets:
            path = bundle_directory / w
            with path.open('r') as f:
                widget = yaml.load(f, Loader=yaml.FullLoader)
                widget['customUi'] = (
                        path.parent / widget['customUiPath']).read_text()
                self._client.update_widget(widget)
