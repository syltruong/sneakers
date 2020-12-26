SHELL := /bin/bash

DOCKER_IMAGE_NAME = sneakers
DOCKER_GPU_IMAGE_NAME = sneakers-gpu
PATH_TO_DATA_DIR = /Users/struong/perso/data/sneakers

# install dependencies
.PHONY: install-dependencies
install-dependencies:
	cp bootstrap.req.txt requirements.txt
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker run --rm $(DOCKER_IMAGE_NAME) cat requirements.txt > requirements.txt


.PHONY: install-dependencies-gpu
install-dependencies-gpu:
	cp bootstrap.req.txt requirements.gpu.txt
	docker build -f Dockerfile.gpu -t $(DOCKER_GPU_IMAGE_NAME) .
	docker run --rm $(DOCKER_GPU_IMAGE_NAME) cat requirements.gpu.txt > requirements.gpu.txt


# download sneakers data via the Sneaker Database API
.PHONY: download-sneakers-data
download-sneakers-data:
	mkdir -p $(PATH_TO_DATA_DIR) 
	
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker run \
		--mount type=bind,source="$(PATH_TO_DATA_DIR)",target=/data \
		$(DOCKER_IMAGE_NAME) python -m data.download_data --output_dir /data


# download sneakers images from csv data and paths
.PHONY: download-sneakers-images
download-sneakers-images:	
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker run \
		--mount type=bind,source="$(PATH_TO_DATA_DIR)",target=/data \
		$(DOCKER_IMAGE_NAME) python -m data.download_images --output_dir /data
