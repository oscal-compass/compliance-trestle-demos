# -*- mode:python; coding:utf-8 -*-

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
# See the License for the specific language governing permissions and
# limitations under the License.
"""Script to convert CIS controls spreadsheet into catalogs and profiles based on implementation group."""

import argparse
import datetime
import logging
import pathlib
import sys
from typing import List, Optional
from uuid import uuid4

from ilcli import Command

import pandas as pd

import trestle.oscal.catalog as oscat
import trestle.oscal.common as oscommon
import trestle.oscal.profile as ospro

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


def run(input_xls: pathlib.Path, output_directory: pathlib.Path, cis_version: str) -> int:
    """Run the conversion process."""
    # To be reviewed - this awkward double read is annoying.
    excel_handler = pd.ExcelFile(input_xls)
    df = None
    for key in excel_handler.sheet_names:
        if 'controls' in str(key).lower():
            sheet_name = key

    df = pd.read_excel(input_xls, sheet_name=sheet_name, header=0, dtype=str)
    # goal: output single catalog of controls and subcontrols
    # also - output separate profiles for each of the implementation groups

    # for profiles / implementation groups
    grp1: List[str] = []
    grp2: List[str] = []
    grp3: List[str] = []

    controls: List[oscat.Control] = []

    control = None
    subcontrols = None
    control_prose = ''
    control_key = 'CIS Control'
    sub_control_key = 'CIS Safeguard'
    for _, row in df.iterrows():
        if not pd.isna(row[control_key]):
            if pd.isna(row[sub_control_key]):
                # if has CIS Control entry but no sub-control then it is a new control
                #   if we already have control we mark it complete and add to list
                if control is not None:
                    control.controls = subcontrols
                    control.parts = [oscommon.Part(name='Description', prose=row['Description'])]
                    controls.append(control)
                control = oscat.Control(id=f'control-{row[control_key].strip()}', title=row['Title'])
                subcontrols: List[oscat.Control] = []
            else:
                # if it has both a CIS Control entry and sub-control entry it is a sub-control
                part = oscommon.Part(name='Description', prose=row['Description'])
                cid = f'control-{row[sub_control_key].strip()}'
                subcont = oscat.Control(id=cid, title=row['Title'], class_=row['Asset Type'], parts=[part])
                subcontrols.append(subcont)

                # now add it to corresponding profile / implementation group
                if not pd.isna(row['IG1']):
                    grp1.append(cid)
                if not pd.isna(row['IG2']):
                    grp2.append(cid)
                if not pd.isna(row['IG3']):
                    grp3.append(cid)
        else:
            # if it has no CIS Control entry but it does have title field it is prose for the main control
            if not pd.isna(row['Title']):
                control_prose = row['Title']

    # need to add last one
    control.controls = subcontrols
    control.parts = [oscommon.Part(name='Description', prose=control_prose)]
    controls.append(control)

    cat_metadata = oscommon.Metadata(
        **{
            'title': f'CIS Controls version {cis_version} catalog.',
            'last-modified': datetime.datetime.now().astimezone(),
            'version': cis_version,
            'oscal-version': '1.0.0'
        }
    )

    cat = oscat.Catalog(uuid=str(uuid4()), metadata=cat_metadata, controls=controls)
    catalog_path: pathlib.Path = output_directory / f'CIS_controls_version_{cis_version}_catalog.json'
    cat.oscal_write(catalog_path)

    profile = ospro.Profile(
        uuid=str(uuid4()),
        metadata=oscommon.Metadata(
            **{
                'title': 'CIS Implementation Group 1',
                'version': cis_version,
                'oscal-version': '1.0.0milestone3',
                'last-modified': datetime.datetime.now().astimezone()
            }
        ),
        imports=[ospro.Import(href=catalog_path.name)]
    )

    profile_path: pathlib.Path = output_directory / f'CIS_version_{cis_version}_profile_Implementation_Group_1.json'
    write_profile(profile, grp1, profile_path)

    profile_path: pathlib.Path = output_directory / f'CIS_version_{cis_version}_profile_Implementation_Group_2.json'
    write_profile(profile, grp2, profile_path)

    profile_path: pathlib.Path = output_directory / f'CIS_version_{cis_version}_profile_Implementation_Group_3.json'
    write_profile(profile, grp3, profile_path)


def write_profile(profile: ospro.Profile, control_list: List[str], path: pathlib.Path):
    """Fill in control list and write the profile."""
    include_controls: List[str] = []
    selector = ospro.SelectControl()
    selector.with_ids = control_list
    include_controls.append(selector)
    profile.imports[0].include_controls = include_controls

    profile.oscal_write(path)


def determine_version(file_pth: pathlib.Path) -> Optional[str]:
    """Determine version from a file name or return null."""
    try:
        result = file_pth.name.lower().split('version')[1].strip().split(' ')[0]
        if len(result.strip()) > 0:
            return result
    except Exception:
        return None


class CISConverter(Command):
    """Converter CLI wrapper class."""

    def _init_arguments(self) -> None:
        self.add_argument('-i', '--input', help='', type=pathlib.Path, required=True)
        self.add_argument('-o', '--output', help='', type=pathlib.Path, default=pathlib.Path.cwd())
        self.add_argument('-v', '--cis-version', help='', type=str, default=None)

    def _run(self, args: argparse.Namespace) -> int:
        if not args.cis_version:
            version_str = determine_version(args.input)
        else:
            version_str = args.cis_version

        run(args.input, args.output, version_str)


if __name__ == '__main__':
    sys.exit(CISConverter().run())
