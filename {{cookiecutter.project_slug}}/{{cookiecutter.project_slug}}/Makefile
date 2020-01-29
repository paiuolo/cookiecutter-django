DOCKER=docker
DPATH=${CURDIR}

IMAGE_NAME={{cookiecutter.project_slug}}
VERSION=0.0.1


export DPATH
.PHONY:	build push

build:
	$(DOCKER) build . -f ./compose/production/django/Dockerfile -t paiuolo/${IMAGE_NAME} -t paiuolo/${IMAGE_NAME}:${VERSION}

push:
	$(DOCKER) push paiuolo/${IMAGE_NAME}:${VERSION}
	$(DOCKER) push paiuolo/${IMAGE_NAME}:latest
