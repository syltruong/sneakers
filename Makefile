SHELL := /bin/bash

DOCKER_IMAGE_NAME = sneakers
DOCKER_GPU_IMAGE_NAME = sneakers-gpu
#PATH_TO_DATA_DIR = /Users/struong/perso/data/sneakers
PATH_TO_DATA_DIR = /home/struong/data/sneakers
PATH_TO_LOG_DIR = /home/struong/project/sneakers

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


# refer to https://github.com/pytorch/pytorch/issues/2244
# increasing shared memory size in `docker run` as dataloader workers depend on this
.PHONY: train-simclr-gpu
train-simclr-gpu:
	docker build -f Dockerfile.gpu -t $(DOCKER_GPU_IMAGE_NAME) .
	docker run \
		-u `id -u`:`id -g` \
		--gpus all \
		--shm-size 16G \
		--mount type=bind,source="$(PATH_TO_DATA_DIR)",target=/data \
		--mount type=bind,source="$(PATH_TO_LOG_DIR)",target=/logs \
		$(DOCKER_GPU_IMAGE_NAME) python -m training.main \
			--data_dir /data \
			--log_dir /logs \
			--input_height 64 \
			--batch_size 64 \
			--learning_rate 1e-2 \
			--gpus 8 \
			--num_workers 48 \
			--max_epochs 100


.PHONY: tensorboard
tensorboard:
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker run \
		--mount type=bind,source="$(PATH_TO_LOG_DIR)",target=/logs \
		-p 6006:6006 \
		$(DOCKER_IMAGE_NAME) tensorboard --logdir /logs --bind_all