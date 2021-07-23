# -*- mode:python; coding:utf-8 -*-

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
"""Simple script to create a catalog.

This script does three things:
1) Fails to create a catalog when not passing the required variables
2) Creates a catalog
3) Writes it out to json using oscal_write
"""

import logging
import pathlib
import sys
from datetime import datetime
from uuid import uuid4

from trestle.oscal.catalog import Catalog
from trestle.oscal.common import Metadata

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('Deliberately fail to make a Catalog properly')

try:
    c = Catalog()
except Exception as e:
    logger.error(e)

logger.info('')
logger.info('Make some Metadata')
m = Metadata(title='my cool catalog', last_modified=datetime.now().astimezone(), version='0.0.1', oscal_version='1.0.0')
logger.info(m)

logger.info('')
logger.info('Make a Catalog')
c = Catalog(metadata=m, uuid=str(uuid4()))
logger.info(c)

logger.info('')
logger.info('Writing catalog')
c.oscal_write(pathlib.Path('catalog.json'))
