#!/usr/bin/env bash

# set environment variables
. ./set_env.sh

docker run -e "CLIENT_ID=${CLIENT_ID}" \
    -e "CLIENT_SECRET=${CLIENT_SECRET}" \
    -e "ENTANDO_USERNAME=${ENTANDO_USERNAME}" \
    -e "ENTANDO_PASSWORD=${ENTANDO_PASSWORD}" \
    -e "TOKEN_URL=${TOKEN_URL}" \
    -e "ENTANDO_CORE_URL=${ENTANDO_CORE_URL}" \
    -v ~/projects/entando-process-driven-plugin/bundle_out:/bundle \
    werbth/entando-bundle-updater:latest
