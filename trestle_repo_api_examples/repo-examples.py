# -*- mode:python; coding:utf-8 -*-

# Copyright (c) 2021 IBM Corp. All rights reserved.
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
"""Simple script to demo repository APIs."""

import logging
import pathlib
import sys

import trestle.core.parser as parser
import trestle.oscal as oscal
from trestle.core.repository import Repository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def demo():
    """Run the demo."""
    trestle_workspace = './trestle-workspace'
    logger.info('')
    logger.info('1. Create Respository object by giving path to initalized trestle repository')
    repo_path = pathlib.Path(trestle_workspace).resolve()
    repo = Repository(repo_path)
    logger.info(f'Respository object created with root as: {repo.root_dir}')

    logger.info('')
    logger.info('2. Parse an existing OSCAL catalog file into OSCAL model object')
    filepath = pathlib.Path('./NIST_SP-800-53_rev4_catalog.json')
    model = parser.parse_file(filepath, None)
    logger.info('File successfully parsed')

    logger.info('')
    logger.info('3. Import the parsed model object imto trestle repository')
    model = repo.import_model(model, 'NIST')
    logger.info(f'A directory {trestle_workspace}/catalogs/NIST/ is created with catalog.json file in it.')
    input('Press <Enter/Return> after checking the directory:')

    logger.info('')
    logger.info('4. Validate the model in repository')
    success = repo.validate_model(oscal.catalog.Catalog, 'NIST')
    logger.info(f'Valid model? {success}')

    logger.info('')
    logger.info('5. Assemble the contents of the model into "dist" directory')
    success = repo.assemble_model(oscal.catalog.Catalog, 'NIST')
    logger.info(f'Model assembled? {success}')
    logger.info(f'A file NIST.json is created in directory {trestle_workspace}/dist/catalogs/')
    input('Press <Enter/Return> after checking:')

    logger.info('')
    logger.info('6. List models of type Catalog')
    models = repo.list_models(oscal.catalog.Catalog)
    logger.info(models)

    logger.info('')
    logger.info('7. Get the model from the repository.')
    logger.info('It creates a ManagedOSCAL object that can be used to perform operations on that specific model')
    model = repo.get_model(oscal.catalog.Catalog, 'NIST')
    logger.info(f'{model.root_dir}, {model.model_name}, {model.model_alias}, {model.model_dir}, {model.filepath}')

    logger.info('')
    logger.info('8. Split Metadata from the model')
    success = model.split(pathlib.Path('catalog.json'), ['catalog.metadata'])
    logger.info(f'Model split? {success}')
    logger.info(f'A file metadata.json is created in directory {trestle_workspace}/catalogs/NIST/catalog/')
    input('Press <Enter/Return> after checking:')

    logger.info('')
    logger.info('9. Merge Metadata back into the model')
    success = model.merge(['catalog.*'])
    logger.info(f'Model merged? {success}')
    logger.info(f'File metadata.json in directory {trestle_workspace}/catalogs/NIST/catalog/ must have been removed.')
    logger.info(
        f'Contents of metadata.json has been merged back in {trestle_workspace}/catalogs/NIST/catalog.json file'
    )
    input('Press <Enter/Return> after checking:')

    logger.info('')
    logger.info('10. Read the model from reporsitory as an OSCAL model object')
    oscal_model = model.read()
    logger.info('Model read')

    logger.info('')
    logger.info('11. Write the OSCAL model object to reporistory')
    success = model.write(oscal_model)
    logger.info('Model written')

    logger.info('')
    logger.info('12. Validate the model')
    success = model.validate()
    logger.info(f'Valid model? {success}')

    logger.info('')
    logger.info('13. Delete the imported model')
    success = repo.delete_model(oscal.catalog.Catalog, 'NIST')
    logger.info(f'Model deleted? {success}')
    logger.info(
        f'The directory {trestle_workspace}/catalogs/NIST and file '
        + f'{trestle_workspace}/dist/catalogs/NIST.json has been deleted.'
    )
    input('Press <Enter/Return> after checking:')

    logger.info('')
    logger.info('Demo complete.')


if __name__ == '__main__':
    demo()
