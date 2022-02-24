# -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2022 IBM Corp. All rights reserved.
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
"""kubernetes-results-to-OSCAL."""
import datetime
import glob
import logging
import pathlib
import uuid
from typing import Any, Dict, List

from trestle.oscal.assessment_results import ControlSelection
from trestle.oscal.assessment_results import LocalDefinitions1
from trestle.oscal.assessment_results import Observation
from trestle.oscal.assessment_results import Result
from trestle.oscal.assessment_results import ReviewedControls
from trestle.oscal.common import InventoryItem
from trestle.oscal.common import Property
from trestle.oscal.common import SubjectReference
from trestle.transforms.results import Results

import yaml

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname).1s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
logger = logging.getLogger(__name__)

_timestamp = datetime.datetime.utcnow().replace(microsecond=0).replace(tzinfo=datetime.timezone.utc).isoformat()


class SourceFolder:
    """Manage source folder."""

    def __init__(self, ifolder: str) -> None:
        """Initialize instance."""
        self.list = glob.glob(ifolder + '*.yaml')
        self.list.sort()

    def __iter__(self):
        """Initialize iterator."""
        self.n = 0
        return self

    def __next__(self):
        """Next."""
        if self.n < len(self.list):
            self.n += 1
            return self.list[self.n - 1]
        else:
            raise StopIteration


class YamlToOscal:
    """Manage YAML to OSCAL transformations."""

    def _ns(self) -> str:
        """Return namespace."""
        return 'https://kubernetes.github.io/compliance-trestle/schemas/oscal/ar/scc'

    def _uuid(self) -> str:
        """Return uuid."""
        return str(uuid.uuid4())

    def _title(self, yaml_data: Dict) -> str:
        """Return title."""
        return self._get_value(yaml_data, ['metadata', 'name'])

    def _description(self, yaml_data: Dict) -> str:
        """Return description."""
        for label in ['wgpolicyk8s.io/engine', 'policy.kubernetes.io/engine']:
            try:
                return self._get_value(yaml_data, ['metadata', 'labels', label])
            except KeyError:
                continue
        return None

    def _control_selections(self) -> List[ControlSelection]:
        """Return control-selection list."""
        rval = []
        rval.append(ControlSelection())
        return rval

    def _reviewed_controls(self) -> ReviewedControls:
        """Return reviewed controls."""
        rval = ReviewedControls(control_selections=self._control_selections())
        return rval

    def _whitespace(self, text: str) -> str:
        """Replace line ends with blanks."""
        return str(text).replace('\n', ' ')

    def _normalize(self, text: str) -> str:
        """Replace slashes with underscores."""
        return text.replace('/', '_')

    def _get_value(self, yaml_data: Dict, keys: List[str]) -> Any:
        """Descend yaml layers to get value for order list of keys."""
        try:
            value = yaml_data
            for key in keys:
                value = value[key]
        except KeyError:
            raise KeyError
        return value

    def _add_prop(self, props: List[Property], name: str, yaml_data: Dict, keys: List[str]) -> Property:
        """Add property to list."""
        try:
            value = self._get_value(yaml_data, keys)
            prop = Property(name=self._normalize(name), value=self._whitespace(value))
            props.append(prop)
            return prop
        except KeyError:
            return None

    def _add_prop_with_ns(self, props: List[Property], name: str, yaml_data: Dict, keys: List[str], ns, class_) -> None:
        """Add property with ns and class to list."""
        try:
            value = self._get_value(yaml_data, keys)
            prop = Property(name=self._normalize(name), value=self._whitespace(value), ns=ns, class_=class_)
            props.append(prop)
            return prop
        except KeyError:
            return None

    def _get_result_observations(self, yaml_data: Dict, subjects: List[SubjectReference]) -> List[Observation]:
        """Return result observations list."""
        observations = []
        results = yaml_data['results']
        for result in results:
            observation = Observation(
                uuid=self._uuid(),
                description=self._description(yaml_data),
                methods=['TEST-AUTOMATED'],
                props=[],
                subjects=subjects,
                collected=_timestamp
            )
            for key in result.keys():
                if key in ['properties']:
                    props = result[key]
                    for prop in props:
                        self._add_prop(observation.props, 'results.' + key + '.' + prop, props, [prop])
                elif key in ['resources']:
                    resources = result[key][0]
                    for resource in resources:
                        self._add_prop(observation.props, 'results.' + key + '.' + resource, resources, [resource])
                else:
                    class_map = {'policy': 'scc_rule', 'result': 'scc_result', 'message': 'scc_description'}
                    if key in class_map.keys():
                        self._add_prop_with_ns(
                            observation.props, 'results.' + key, result, [key], self._ns(), class_map[key]
                        )
                    else:
                        self._add_prop(observation.props, 'results.' + key, result, [key])
            observations.append(observation)
        return observations

    def _get_result_properties(self, yaml_data: Dict) -> List[Property]:
        """Return result property list."""
        props = []
        for key in [
                'apiVersion',
                'kind',
                'metadata.namespace',
                'metadata.annotations.name',
                'metadata.annotations.category',
                'metadata.annotations.file',
                'metadata.annotations.version',
                'summary.pass',
                'summary.fail',
                'summary.warn',
                'summary.error',
                'summary.skip',
        ]:
            self._add_prop(props, key, yaml_data, key.split('.'))
        return props

    def _get_local_definitions(self, yaml_data: Dict) -> LocalDefinitions1:
        """Return local definitions."""
        try:
            props = []
            for key in yaml_data['scope']:
                compound_key = 'scope.' + key
                class_map = {'namespace': 'scc_scope'}
                if key in class_map.keys():
                    self._add_prop_with_ns(
                        props, compound_key, yaml_data, compound_key.split('.'), self._ns(), class_map[key]
                    )
                else:
                    self._add_prop(props, compound_key, yaml_data, compound_key.split('.'))
            inventory_item = InventoryItem(uuid=self._uuid(), description='inventory', props=props)
            rval = LocalDefinitions1()
            rval.inventory_items = [inventory_item]
        except KeyError:
            rval = None
        return rval

    def _get_subjects(self, local_definitions: List[LocalDefinitions1]) -> List[SubjectReference]:
        """Return subject list."""
        try:
            subjects = []
            for item in local_definitions.inventory_items:
                subject_reference = SubjectReference(subject_uuid=item.uuid, type='inventory-item')
                subjects.append(subject_reference)
        except AttributeError:
            subjects = None
        except TypeError:
            subjects = None
        return subjects

    def _get_result(self, yaml_data: Dict) -> Result:
        """Return result."""
        result = Result(
            uuid=self._uuid(),
            title=self._title(yaml_data),
            description=self._description(yaml_data),
            start=_timestamp,
            reviewed_controls=self._reviewed_controls(),
        )
        result.prop = self._get_result_properties(yaml_data)
        result.local_definitions = self._get_local_definitions(yaml_data)
        subjects = self._get_subjects(result.local_definitions)
        result.observations = self._get_result_observations(yaml_data, subjects)
        return result

    def transform(self, yaml_data_list: List[Dict]) -> Results:
        """Transform yaml to OSCAL json."""
        results = Results()
        for yaml_data in yaml_data_list:
            result = self._get_result(yaml_data)
            results.__root__.append(result)
        return results


def main():
    """Transform k8s results to OSCAL."""
    ytoo = YamlToOscal()
    # output
    ofolder = 'oscal'
    opath = pathlib.Path(ofolder)
    opath.mkdir(parents=True, exist_ok=True)
    # input
    ifolder = 'wg-policy-prototypes/policy-report/samples/'
    source_folder = SourceFolder(ifolder)
    # create output OSCAL json file for each input k8s yaml file
    try:
        for ifile in source_folder:
            ipath = pathlib.Path(ifile)
            ofile = opath / (ipath.stem + '.json')
            yaml_data = []
            with open(ipath, 'r', encoding='utf-8') as yaml_file:
                for yaml_section in yaml.safe_load_all(yaml_file):
                    yaml_data.append(yaml_section)
                results = ytoo.transform(yaml_data)
                results.oscal_write(pathlib.Path(ofile))
                logger.info(f'created: {ofile.name}')
    except yaml.YAMLError as e:
        logger.error(e)
        raise Exception(f'Exception processing {ipath.name}')


if __name__ == '__main__':
    main()
