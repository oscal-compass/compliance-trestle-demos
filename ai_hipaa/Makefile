
.ONESHELL:
SHELL := /bin/bash

PYTHON := python
MKDIR_P := mkdir -p

SOURCE := $(HOME)/venv.oscal-agentic
SOURCE_ACTIVATE := $(SOURCE)/bin/activate

ROOT_DIR := $(shell pwd)

PROMPT_ASST := $(ROOT_DIR)/prompts/catalog_assistant.md

TRESTLE_WS := $(ROOT_DIR)/trestle.ws

# -----

all: hipaa
	
# -----

HIPAA := hipaa

PROMPT_USER_HIPAA := prompts/catalog_user_hipaa.md

TRESTLE_WS_HIPAA := trestle.ws/catalogs/$(HIPAA)
TRESTLE_WS_HIPAA_CATALOG := $(TRESTLE_WS_HIPAA)/catalog.json

HIPAA_WORK := work
HIPAA_PYTHON := $(HIPAA_WORK)/xlsx_to_catalog.py

hipaa: hipaa-clean hipaa-prereq hipaa-start hipaa-llm hipaa-docker hipaa-validate hipaa-end

hipaa-clean:
	rm -f $(TRESTLE_WS_HIPAA_CATALOG)

hipaa-prereq: venv

hipaa-start:
	@echo "Start HIPAA: $(shell date +'%Y-%m-%d %H:%M:%S')"

hipaa-end:
	@echo "End HIPAA: $(shell date +'%Y-%m-%d %H:%M:%S')"

hipaa-llm:
	@echo "Skip llm"

hipaa-docker:
	${MKDIR_P} $(TRESTLE_WS_HIPAA); \
	docker build -t my-image .
	docker run --name my-container my-image
	docker cp my-container:/app/data/catalog.json $(TRESTLE_WS_HIPAA)
	docker stop my-container
	docker rm my-container

hipaa-validate: venv
	source $(SOURCE_ACTIVATE); \
	cd $(TRESTLE_WS); \
	trestle validate -f catalogs/$(HIPAA)/catalog.json

# -----
	
clean: venv.clean

venv.clean:
	rm -fr $(SOURCE)

.SILENT: venv
venv:
	if [ ! -d $(SOURCE) ]; then \
		${MKDIR_P} $(SOURCE); \
		python -m venv $(SOURCE); \
		source $(SOURCE_ACTIVATE); \
		pip install -r requirements.txt; \
	fi

