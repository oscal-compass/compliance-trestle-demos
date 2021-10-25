#!/usr/bin/env python3
# # -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2020 IBM Corp. All rights reserved.
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
# limitations under the License.
"""Create ISM catalogs.

This script is used to convert Australian Government Information Security Manual (ISM) into OSCAL formats.
The ISM is the equivalent of NIST 800-53 / FedRAMP / IL6 and similar documents in the USA. The goal is to produce a
similar set OSCAL documents to what NIST and FedRAMP are currently publishing.

It does this via pulling the ISM xml doc and creating:

1 Catalog for all the controls
4 profiles (Official, protected, secret, TS)

Ideally this would be a cron job based script, however, as ACSC publish revisions
with specific names this would need to be discovered by crawling. This will be a potential future enhancement.

This script pulls down the controls in a 'dumb' way from the xml to get the actual controls. A full featured catalog
will need to parse appropriate word / xml documents to provide groups /guidance.
"""
import io
import json
import logging
import pathlib
import sys
import urllib.request
import zipfile
from datetime import datetime
from uuid import uuid4

from ilcli import Command

import trestle.oscal.catalog as catalog
import trestle.oscal.common as common
import trestle.oscal.profile as profile

import xmltodict

# Globally define logging behaviour.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

remarks_tuple = '\n'.join(
    [
        'This is not an official version of the Australian Government Information Security Manual.',
        '',
        'Find the official versions here: https://www.cyber.gov.au/acsc/view-all-content/ism',
        'This content was generated using scrips/ISM/ISM.py'
    ]
)


class ISMManager():
    """ISMManager a class to manage conversion of ISM artifacts into OSCAL."""

    def __init__(self):
        """Initialize ISM manager. No required parameters."""
        self._profile_controls = {'OFFICIAL': [], 'PROTECTED': [], 'SECRET': [], 'TOP_SECRET': []}
        self._profiles = {}

    def fetch_ism(self, url):
        """Fetch an Australian government ISM and covert to a dict."""
        logger.debug('Fetching ISM from: ' + url)
        request_url = urllib.request.urlopen(url)
        document = request_url.read()
        zipfile_content = zipfile.ZipFile(io.BytesIO(document))
        content_list = zipfile_content.namelist()
        xml_files = [x for x in content_list if '.xml' in x]
        assert len(xml_files) == 1
        self.ism_xml = xmltodict.parse(zipfile_content.open(xml_files[0]).read())

    def _populate_control_list(self, control, raw_id):
        """Populate control lists based on a dict from the xml version of the ISM."""
        # TODO: Really not pythonic but anyway.
        control_id = 'control-' + raw_id

        for security_level in self._profile_controls.keys():
            # Dealing with schema changes 'Yes' and 'true' appear to both be valid options.
            if control[security_level].lower() == 'yes' or control[security_level].lower() == 'true':
                self._profile_controls[security_level].append(control_id)

    def _probe_for_keys(self, ism_control):
        """Probe for the appropriate keys for l2 groups based on whether or not section exists."""
        l2_group_key = 'Section'

        if l2_group_key not in ism_control.keys():
            l2_group_key = 'Topic'
        return l2_group_key

    def _name_clean(self, name: str) -> str:
        """Normalize string to ncname format."""
        return name.strip().lower().replace(' ', '_').replace('/', '-')

    def create_ism_catalog(self, version: str) -> None:
        """Parse ISM object and create a catalog."""
        m = common.Metadata(
            **{
                'title': 'Australian Government Information Security manual',
                'last-modified': datetime.now().astimezone(),
                'version': version,
                'oscal-version': '1.0.0',
                'remarks': remarks_tuple
            }
        )
        ism_catalog = catalog.Catalog(metadata=m, uuid=str(uuid4()))

        # Create basic metadata:
        ism_controls = self.ism_xml['ISM']['Control']
        l2_group_key = self._probe_for_keys(ism_controls[0])
        """
        Approach:
            - Two levels of groups - no sub controls.
            - below this will be parts
        """
        # Get list of top level controls
        tl_group_titles = set(map(lambda x: x['Guideline'], ism_controls))
        groups = []
        for tl_group_name in tl_group_titles:
            group = catalog.Group(id=self._name_clean(tl_group_name), title=tl_group_name)
            # now add l2 groups
            control_subset = list(filter(lambda x: x['Guideline'] == tl_group_name, ism_controls))
            # get set l2 group names.
            l2_group_titles = set(map(lambda x: x[l2_group_key], control_subset))
            l2_groups = []
            for l2_group_name in l2_group_titles:
                clean_id = self._name_clean(l2_group_name)
                l2_group = catalog.Group(id=clean_id, title=l2_group_name)
                # Now identify and add the controls
                oscal_controls = []
                l2_control_subset = list(filter(lambda x: x[l2_group_key] == l2_group_name, control_subset))
                # now we can create and add controls.
                # TODO: Make more pythonic
                for ism_control in l2_control_subset:
                    raw_id = ism_control['Identifier']

                    description = ism_control['Description']
                    topic = ism_control['Topic']
                    # make description the part statement
                    statement_part = common.Part(id='control-' + raw_id + '-stmt', name='statement', prose=description)
                    # this is very minimial
                    oscal_control = catalog.Control(
                        id='control-' + raw_id, title=topic + ' ' + raw_id, parts=[statement_part]
                    )
                    self._populate_control_list(ism_control, raw_id)
                    oscal_controls.append(oscal_control)
                l2_group.controls = oscal_controls
                l2_groups.append(l2_group)
            group.groups = l2_groups
            groups.append(group)
        ism_catalog.groups = groups
        self._ism_catalog = ism_catalog

    def create_ism_profiles(self, revision_date, uri='./ISM_catalog.yaml'):
        """Create profile for each ISM environment."""
        for security_level in self._profile_controls.keys():
            ism_profile = profile.Profile(
                uuid=str(uuid4()),
                metadata=common.Metadata(
                    **{
                        'title': 'Australian Government Information Security Manual profile for ' + security_level,
                        'version': revision_date,
                        'oscal-version': '1.0.0',
                        'last-modified': datetime.now().astimezone(),
                        'remarks': remarks_tuple
                    }
                ),
                imports=[profile.Import(href=uri)]
            )
            controls_list = self._profile_controls[security_level]
            ism_profile.imports[0].include_controls = self._populate_import_include(controls_list)
            self._profiles[security_level] = ism_profile

    def _populate_import_include(self, control_list):
        include_controls = []
        selector = profile.SelectControlById()
        selector.with_ids = control_list
        include_controls.append(selector)
        return include_controls

    def write_catalog(self, catalogs_path, ism_name):
        """Wrap and write oscal catalog object."""
        ism_dir_path = catalogs_path / ism_name
        ism_dir_path.mkdir(exist_ok=True)
        ism_file_path = ism_dir_path / 'catalog.json'
        self._ism_catalog.oscal_write(ism_file_path)

    def write_profiles(self, profiles_dir, ism_name):
        """Write out all profiles."""
        for security_level in self._profiles.keys():
            profile_dir = profiles_dir / (ism_name + '_' + security_level)
            profile_dir.mkdir(exist_ok=True)
            profile_path = profile_dir / 'profile.json'
            self._profiles[security_level].oscal_write(profile_path)


class ISM(Command):
    """
    Convert the Australian goverment information security manual (in various versions) into catalogs and profiles.

    This CLI has presumptions on resource structures that are returned.

    Please note that this project current presumes information about the project structure.
    """

    def _init_arguments(self):
        self.add_argument('-r', '--root-dir', help='Trestle project root.', default='./')

    def _run(self, args):
        # little test
        root_dir = pathlib.Path(args.root_dir).resolve()
        catalogs_dir = root_dir.joinpath('catalogs').resolve()
        profiles_dir = root_dir.joinpath('profiles').resolve()
        ism_json_file = root_dir.joinpath('scripts/ISM/ism_editions.json').resolve()

        if not root_dir.exists():
            logger.error('Root trestle project does not exist')
            return 1
        if not catalogs_dir.exists():
            logger.error('Catalogs directory does not exist.')
            return 1

        if not profiles_dir.exists():
            logger.error('Profiles directory does not exist.')
            return 1

        ism_versions = json.load(ism_json_file.open())

        for ism_file in ism_versions['isms']:
            # ISM file format: 'ISM - List of Security Controls (August 2019).xml'
            logger.info(ism_file)
            url = ism_file['version_url']
            ism_manager = ISMManager()
            ism_manager.fetch_ism(url)
            revision_date = ism_file['version_name'].split()
            revision_string = revision_date[0] + '_' + revision_date[1]
            logger.info(f'Revision date: {revision_date}')
            logger.info(f'Revision string: {revision_string}')
            logger.info(revision_string)
            ism_name = 'ISM_' + revision_string

            ism_manager.create_ism_catalog(revision_string)
            # This is presumed to be relative for now to the catalog repo based on this
            ism_manager.write_catalog(catalogs_dir, ism_name)
            ism_manager.create_ism_profiles(revision_string, 'trestle://' + ism_name + '/catalog.json')
            ism_manager.write_profiles(profiles_dir, ism_name)


if __name__ == '__main__':
    sys.exit(ISM().run())
