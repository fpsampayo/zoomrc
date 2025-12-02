ZoomRc Qgis Plugin
==================

This plugin alows the user to zoom to a Spanish Cadastre reference.

## Make the package to upload to qgis plugins site

```shell
make package
```

## Run plugin on qgis version to test

Inside docker folder, exists a `docker-compose.yml` with a qgis service pointing to the latest ltr version. 
You can change to other than exists on [qgis offical docker hub image](https://hub.docker.com/r/qgis/qgis).

Executing `start_qgis.sh` will launch that version of QGIS with the sigpac-downloader plugin configured.