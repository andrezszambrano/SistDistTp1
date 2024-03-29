SHELL := /bin/bash
PWD := $(shell pwd)

GIT_REMOTE = github.com/7574-sistemas-distribuidos/docker-compose-init

default: build

all:

deps:
	go mod tidy
	go mod vendor

build: deps
	GOOS=linux go build -o bin/client github.com/7574-sistemas-distribuidos/docker-compose-init/client
.PHONY: build

docker-image:
	docker build -f ./rabbitmq/Dockerfile -t "rabbitmq:latest" .
	docker build -f ./server/server_common/Dockerfile -t "base_python_image:latest" .
	docker build -f ./server/client_main_api_processor/Dockerfile -t "client_main_api_processor:latest" .
	docker build -f ./server/data_distributor_processor/Dockerfile -t "data_distributor_processor:latest" .
	docker build -f ./server/weather_processor/Dockerfile -t "weather_processor_image:latest" .
	docker build -f ./server/montreal_filterer/Dockerfile -t "montreal_filterer:latest" .
	docker build -f ./server/duplicated_processor/Dockerfile -t "duplicated_processor:latest" .
		docker build -f ./server/years_filterer/Dockerfile -t "years_filterer:latest" .
	docker build -f ./server/query_processor/Dockerfile -t "query_processor:latest" .
	docker build -f ./server/result_processor/Dockerfile -t "result_processor:latest" .
	docker build -f ./client/Dockerfile -t "client:latest" .
	docker build -f ./server/montreal_distance_processor/Dockerfile -t "montreal_distance_processor:latest" .

	# Execute this command from time to time to clean up intermediate stages generated 
	# during client build (your hard drive will like this :) ). Don't left uncommented if you 
	# want to avoid rebuilding client image every time the docker-compose-up command 
	# is executed, even when client code has not changed
	# docker rmi `docker images --filter label=intermediateStageToBeDeleted=true -q`
.PHONY: docker-image

docker-compose-up: docker-image docker-compose-down
	docker compose -f docker-compose-dev.yaml up -d --build
.PHONY: docker-compose-up

docker-compose-up-without-build: docker-image
	docker compose -f docker-compose-dev.yaml up -d
.PHONY: docker-compose-up-without-build

docker-compose-test: docker-image
	docker compose -f docker-compose-dev.yaml run server-test
.PHONY: docker-compose-up

docker-compose-down:
	docker compose -f docker-compose-dev.yaml stop -t 1
	docker compose -f docker-compose-dev.yaml down
.PHONY: docker-compose-down

docker-compose-stop:
	docker compose -f docker-compose-dev.yaml stop -t 5
.PHONY: docker-compose-stop

docker-compose-logs:
	docker compose -f docker-compose-dev.yaml logs -f
.PHONY: docker-compose-logs
