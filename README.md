# Sneakers

Explore sneakers database

## Commands

### `make install-dependencies`

To install dependencies from `./bootstrap.req.txt` and `pip freeze` to `requirements.txt`.
This is to use `pip` as the package manager and pin python library versions.

### `make download-sneakers-data`

To download data from the Sneakers Database API and dump it as a csv in a local data folder.
The path of the data folder is to be modified in the `Makefile`->`PATH_TO_DATA_DIR`.

### `make download-sneakers-images`

To download sneaker images (thumbnails) from the abovementioned csv file, to a local folder.
The path of the data folder is to be modified in the `Makefile`->`PATH_TO_DATA_DIR`.
