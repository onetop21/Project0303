#make check : checking docker environment.
#make build : docker build, (stage1: flutter build, stage2 python run)
#make install : docker run s3, mongodb, redis, project
#make uninstall : docker stop

APP_NAME=Project0303

UPPER_NAME=$(shell echo $(APP_NAME) | tr [a-z] [A-Z])
LOWER_NAME=$(shell echo $(APP_NAME) | tr [A-Z] [a-z])

DOCKER_INSTALLED=$(shell which docker >> /dev/null && docker version -f {{.Server}} >> /dev/null && echo 1)
DOCKER_VERSION=$(shell docker version -f {{.Server.Version}})
DOCKER_PLATFORM=$(shell docker version -f '{{.Server.Os}}/{{.Server.Arch}}')

# TAG (HASH[:7]) [DATE]
GIT_TAG=$(shell git describe --abbrev=0 --tags)
GIT_COMMIT=$(shell git log -1 --format=%H | cut -c1-7)
GIT_DATE=$(shell git log -1 --format=%cd) 

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
.DEFAULT_GOAL := help

check: ## Install docker environment.
ifeq ($(DOCKER_INSTALLED),1)
	@echo "[✔] \033[32mDocker Installed.\033[0m"
	@echo "    Docker Version:  \033[33m$(DOCKER_VERSION)\033[0m"
	@echo "    Docker Platform: \033[33m$(DOCKER_PLATFORM)\033[0m"
else
	@echo "[❌] \033[31mDocker Installed.\033[0m"
	@echo "     \033[33mPlease visit https://docs.docker.com/get-docker/ and install docker.\033[0m"
endif

debug: ## Build project and run on local environment.
	@cd frontend;flutter build web --release
	@python service
    
build: ## Build and package project to image.
	@docker build -t onetop21/$(LOWER_NAME):$(GIT_TAG) .

clean: ## Clear built image.
	@docker rmi onetop21/$(LOWER_NAME):$(GIT_TAG) -f >> /dev/null

db-start: ## Start databases on docker.
	@docker run -d --name minio -p 9000:9000 -e MINIO_ACCESS_KEY=$(UPPER_NAME) -e MINIO_SECRET_KEY=$(UPPER_NAME) minio/minio server /data >> /dev/null
	@docker run -d --name mongo -p 27017:27017 mongo >> /dev/null

db-resume: ## Resume databases on docker.
	@docker start minio mongo

db-status: ## Show status of databases.
	@docker ps --filter name=mongo --filter name=minio

db-pause: ## Pause databases on docker.
	@echo "Wait a minute..."
	@docker stop minio mongo >> /dev/null
	echo "Done."

db-stop: ## Stop databases on docker.
	@echo "Wait a minute..."
	@docker stop minio mongo | xargs docker rm >> /dev/null
	@echo "Done."

install: ## Install project to docker.
	@docker run -d --name $(LOWER_NAME) -e MONGO_HOST=mongo --link minio:minio --link mongo:mongo -p 8080:8080 onetop21/$(LOWER_NAME):$(GIT_TAG) >> /dev/null
	@echo "\033[1m$(APP_NAME) $(GIT_TAG)[$(GIT_COMMIT)] at http://$(shell hostname -I | awk '{print $$1}'):8080/\033[0m"

uninstall: ## Uninstall project from docker.
	@echo "Wait a minute..."
	@docker stop $(LOWER_NAME) | xargs docker rm >> /dev/null
	@echo "Done."

update: ## Update project to new version.
	@echo "Wait a minute..."
	@docker stop $(LOWER_NAME) | xargs docker rm >> /dev/null
	@docker run -d --name $(LOWER_NAME) -e MONGO_HOST=mongo --link minio:minio --link mongo:mongo -p 8080:8080 onetop21/$(LOWER_NAME):$(GIT_TAG) >> /dev/null

logs: ## Show logs.
	@docker logs -f -t $(LOWER_NAME)

version: ## Output the current version
	@echo "\033[33mGit Version: \033[37m$(GIT_TAG) \033[0m"
	@echo "\033[33mGit Commit: \033[37m$(GIT_COMMIT) \033[34m[$(GIT_DATE)]\033[0m"
#@printf "\033[33mGit Version: \033[37m$(GIT_TAG) \033[34m[$(GIT_COMMIT)] \033[35m$(GIT_DATE)\033[0m\n"
	
help: ## This help.
	@echo "\033[1m\033[32m$(APP_NAME) Makefile \033[35m[$(GIT_TAG)]\033[0m"
	@echo "\033[33mCommands:\033[0m"
#@sed -e 's/$$(APP_NAME)/"$(APP_NAME)"/g' Makefile config.env | awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


