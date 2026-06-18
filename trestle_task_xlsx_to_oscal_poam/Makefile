# Copyright (c) 2025 The OSCAL Compass Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Makefile

.ONESHELL:
SHELL := /bin/bash

SOURCE_INIT = /tmp/venv.trestle
SOURCE_INIT = /home/degenaro/venv-set/venv.poam
SOURCE = $(SOURCE_INIT)

all: venv ws poam

.SILENT: venv
venv:
	if [ ! -d $(SOURCE_INIT) ]; then \
		echo "=> create python virtual environment"; \
		python -m venv $(SOURCE_INIT); \
		source $(SOURCE_INIT)/bin/activate; \
		echo "=> install prereqs"; \
		python -m pip install -q --upgrade pip setuptools; \
		python -m pip install -q compliance-trestle; \
	fi

ws:
	source $(SOURCE)/bin/activate; \
	mkdir -p trestle.ws; \
	cd trestle.ws; \
	trestle init;
	
poam:
	echo "=> create POAM from .xlsx"; \
	source $(SOURCE)/bin/activate; \
	cd trestle.ws; \
	trestle task xlsx-to-oscal-poam --config ../demo-xlsx-to-oscal-poam.config
	
clean: clean-venv

clean-venv:
	rm -fr $(SOURCE_INIT)

