# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# include parameters that configure our deployment
include .env
cert_files=secrets/ssl.pem secrets/ssl.key

.DEFAULT_GOAL=build

network:
	@docker network inspect $(DOCKER_NETWORK_NAME) >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)

volumes:
	@docker volume inspect $(DATA_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DATA_VOLUME_HOST)
	@docker volume inspect $(DB_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DB_VOLUME_HOST)

self-signed-cert:
        # make a self-signed cert

secrets/postgres.env:
	@echo "Generating postgres password in $@"
	@echo "POSTGRES_PASSWORD=$(shell openssl rand -hex 32)" > $@

secrets/oauth.env:
	@echo "Need oauth.env file in secrets with GitHub parameters"
	@exit 1

secrets/ssl.pem:
	@echo "Need an SSL certificate in secrets/ssl.pem"
	@exit 1

secrets/ssl.key:
	@echo "Need an SSL key in secrets/ssl.key"
	@exit 1

hub/userlist:
	@echo "Add usernames, one per line, to hub/userlist, such as:"
	@echo "    zoe admin"
	@echo "    wash"
	@exit 1

check-files: hub/userlist $(cert_files) secrets/oauth.env secrets/postgres.env

pull: 
	docker pull $(DOCKER_NOTEBOOK_IMAGE)

notebook_image: pull
	docker build -t $(LOCAL_NOTEBOOK_IMAGE) \
		--build-arg JUPYTERHUB_VERSION=$(JUPYTERHUB_VERSION) \
		singleuser

build: check-files network volumes
	docker-compose build

.PHONY: network volumes check-files notebook_image build
