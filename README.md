# Entando Bundle Updater

Update/create Entando components on Entando Core from a bundle.

Use this command to run the docker image:

```bash
docker run -e "CLIENT_ID=${CLIENT_ID}" \
    -e "CLIENT_SECRET=${CLIENT_SECRET}" \
    -e "ENTANDO_USERNAME=${ENTANDO_USERNAME}" \
    -e "ENTANDO_PASSWORD=${ENTANDO_PASSWORD}" \
    -e "TOKEN_URL=${TOKEN_URL}" \
    -e "ENTANDO_CORE_URL=${ENTANDO_CORE_URL}" \
    -v ./bundle_out:/bundle \
    werbth/entando-bundle-updater:latest
```
