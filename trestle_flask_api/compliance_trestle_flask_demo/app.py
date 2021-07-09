# -*- mode:python; coding:utf-8 -*-  noqa: D100

# Copyright (c) 2021 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Demonstration flask application integrating trestle."""

import logging
import sys
from dataclasses import dataclass

from flask import Flask, request

from flask_pydantic import validate

import trestle.oscal.catalog

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

app = Flask('trestle-demo-app')


@dataclass
class Config:
    """Config for flask-pydantic."""

    FLASK_PYDANTIC_VALIDATION_ERROR_STATUS_CODE: int = 422


app.config.from_object(Config)


@app.route('/oscal/catalog', methods=['POST'])
@validate(body=trestle.oscal.catalog.Catalog)
def post():
    """Consume catalog and log."""
    logger.info(request.body_params)
    return request.body_params.metadata.json(exclude_none=True, by_alias=True, indent=2)
