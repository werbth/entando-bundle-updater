import base64
import logging
import os

import yaml

from entando_core_client import EntandoClient


class Loader:

    def __init__(self, url, access_token):
        self._client = EntandoClient(url, access_token)

    def load(self, bundle_directory):
        logging.info("Start processing main descriptor")
        with (bundle_directory / "descriptor.yaml").open('r') as descriptor:
            descriptor_yaml = yaml.load(descriptor, Loader=yaml.FullLoader)

            # upload resources
            descriptor_code = descriptor_yaml['code']
            self._upload_resources(bundle_directory, descriptor_code)

            # load widgets
            widgets = descriptor_yaml['components']['widgets']
            self._load_widgets(bundle_directory, widgets)

            # load fragments
            fragments = descriptor_yaml['components']['fragments']
            self._load_fragments(bundle_directory, fragments)

            # load page models
            page_models = descriptor_yaml['components']['pageModels']
            self._load_page_models(bundle_directory, page_models)

    def _upload_resources(self, bundle_directory, descriptor_code):
        logging.info("Uploading resources -------")
        path = bundle_directory / "resources"
        created_directories = []
        for r, d, f in os.walk(path):
            for file in f:
                with open(os.path.join(r, file), 'rb') as file_resource:
                    base_path = os.path.join(descriptor_code,
                                             r.replace(str(path) + "/", ""))
                    if base_path not in created_directories:
                        self._client.create_directory(base_path)
                        created_directories.append(base_path)
                    encoded_resource = base64.b64encode(file_resource.read())
                    resource = {
                        'base64': encoded_resource.decode('utf-8'),
                        'filename': file,
                        'path': os.path.join(base_path, file),
                        'protectedFolder': False
                    }
                    self._client.upload_resource(resource)

    def _load_widgets(self, bundle_directory, widgets):
        logging.info("Loading widgets -------")
        for w in widgets:
            path = bundle_directory / w
            with path.open('r') as f:
                widget = yaml.load(f, Loader=yaml.FullLoader)
                widget['customUi'] = (
                        path.parent / widget['customUiPath']).read_text()
                self._client.update_widget(widget)

    def _load_fragments(self, bundle_directory, fragments):
        logging.info("Loading fragments -------")
        for fragment in fragments:
            path = bundle_directory / fragment
            with path.open('r') as f:
                fragment_yaml = yaml.load(f, Loader=yaml.FullLoader)
                fragment_yaml['guiCode'] = (
                        path.parent / fragment_yaml['guiCodePath']).read_text()
                self._client.update_fragment(fragment_yaml)

    def _load_page_models(self, bundle_directory, page_models):
        logging.info("Loading page models -------")
        for page_model in page_models:
            path = bundle_directory / page_model
            with path.open('r') as f:
                pm_yaml = yaml.load(f, Loader=yaml.FullLoader)
                pm_yaml['template'] = (
                        path.parent / pm_yaml['templatePath']).read_text()
                pm_yaml['descr'] = pm_yaml['description']
                if 'configuration' in pm_yaml and 'frames' in pm_yaml[
                    'configuration']:
                    for frame in pm_yaml['configuration']['frames']:
                        frame['descr'] = frame['description']
                self._client.update_page_model(pm_yaml)
