SRC=$(shell find . -name "*.py"  )

GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null)
GIT_BRANCH_CLEAN := $(shell echo $(GIT_BRANCH) | sed -e "s/[^[:alnum:]]/-/g")
DOCKER_IMAGE := behave-dev$(if $(GIT_BRANCH_CLEAN),:$(GIT_BRANCH_CLEAN))

DOCKER_BUILD_ARGS ?= --force-rm
DOCKERFILE ?= Dockerfile

DOCKER_MOUNT := -v "$(CURDIR)":"/src/app"
DOCKER_FLAGS := docker run --rm -it $(DOCKER_MOUNT) #-u $(shell id -u) $(DOCKER_MOUNT)

DOCKER_RUN := $(DOCKER_FLAGS) "$(DOCKER_IMAGE)"


.PHONY: build
build: ## Build development container.
	docker build $(DOCKER_BUILD_ARGS) -f "$(DOCKERFILE)" -t "$(DOCKER_IMAGE)" .

.PHONY: fmt
fmt: $(SRC) ## Format source code.
	yapf -i --style=google $^
	rm -rf pyling.logs
	for py in $(SRC); do \
		echo $${py} >> pyling.logs 2>&1 && \
		pylint --rcfile=rcfile $${py} >> pyling.logs 2>&1; \
	done || exit 0

.PHONY: shell
shell: build ## Start a shell inside the build environment.
	$(DOCKER_RUN) bash

.PHONY: install
install:
	pip install -e .

.PHONY: tests
tests: install 
	pytest -vv --cache-clear -x
	behave --stop -v

.PHONY: clean
clean:
	rm -rf pkg.egg-info/
	rm -rf pyling.logs
	rm -rf .pytest_cache/
	rm -rf src/pkg/__pycache__/
	rm -rf tests/__pycache__/
