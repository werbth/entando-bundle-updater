#!/bin/env python3
import logging
import os
from pathlib import Path

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from loader import Loader


def get_configuration():
    logging.info("Retrieving configuration from environment")
    return {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'username': os.getenv('ENTANDO_USERNAME'),
        'password': os.getenv('ENTANDO_PASSWORD'),
        'token_url': os.getenv('TOKEN_URL'),
        'entando_url': os.getenv('ENTANDO_CORE_URL'),
        'bundle_directory': os.getenv('BUNDLE_DIRECTORY', '/bundle'),
    }


def get_access_token(env_config):
    logging.info("Authenticating to Keycloak")
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # allow http
    oauth = OAuth2Session(
        client=LegacyApplicationClient(client_id=env_config['client_id']))
    token = oauth.fetch_token(token_url=env_config['token_url'],
                              username=env_config['username'],
                              password=env_config['password'],
                              client_id=env_config['client_id'],
                              client_secret=env_config['client_secret'])
    return token['access_token']


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    config = get_configuration()
    access_token = get_access_token(config)

    bundle_directory = Path(config['bundle_directory'])
    Loader(config['entando_url'], access_token).load(bundle_directory)
