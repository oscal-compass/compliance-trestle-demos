# compliance-trestle-demos

This project captures a number of demos, and sample set of content for [compliance-trestle](https://ibm.github.io/compliance-trestle). Each of the folders in the top level of this project is a self contained demonstration.

These demos are designed to work with trestle version 3.x.x

## Using / management of this repository

This project follows the same methodologies as within the main trestle project in terms of [contributing and developer setup](https://ibm.github.io/compliance-trestle/contributing/mkdocs_contributing/). Please submit [issues here](https://github.com/IBM/compliance-trestle/issues/new/choose) relating to this project.

The top level project itself is a container for a set of demonstrations. At a high level all files are expected to pass:

- mdformat setup
- code-linting for python files (using `flake8`)
- code-formatting for python files (using `yapf`)

All content provided here is 'as is' and is maintained on a best effort basis.

To add a demonstration in addition to opening a PR with the new demonstration in a single folder within the top level project:

- The demonstration folder must have it's own [README.md](ISM_catalog_profile/README.md)
- The list of demonstrations in this folder must be updated.
- A PR must be opened to update

### Demos with CICD

- Some of the demonstrations may integrate with CICD systems (e.g. travis / github actions / circle CI)
- To simplify this project, demonstrations highlighting CICD tooling will be included in this project as a git submodule from an independent repository.

# Demonstrations

## Simple sdk examples.

[This folder](./trestle_sdk_examples) contains a number of small examples for using the trestle OSCAL sdks.

## arc42 architectural template enforcement using trestle author.

[arc42](https://arc42.org/) have created a set open-source architecture documentation templates. This [demonstration](./arc42-author-demo)
uses `trestle author` to enforce use of the (modified) arc42 templates.

A CICD pipeline (using github actions) is used for this demonstration. The full repository, including working CICD is [here](https://github.com/IBM/compliance-trestle-arc42-demo). Read more about the demo [here](https://github.com/IBM/compliance-trestle-arc42-demo).

## Trestle flask microservice demonstation.

`trestle` uses a python library called [pydantic](https://pydantic-docs.helpmanual.io/) to form the underlying OSCAL object models. [flask-pydantic](https://github.com/bauerji/flask_pydantic) introduces a mechanism which integrates pydantic models into flask, providing automated user input validation in one line of code. This demo accepts a catalog as a POSTed object, throwing errors if the catalog does not meet the schema, and returns the catalog in the response.

## Creating a CIS controls catalog from an excel spreadsheet.

The Centre for Internet Security (CIS) produce a number of cross industry standards for IT security including their [platform specific benchmarks](https://www.cisecurity.org/cis-benchmarks/) and a suite of [controls](https://www.cisecurity.org/controls/). [This demo](./CIS_controls) converts a spreadsheet of those controls into a a catalog and three profiles.

## Creating an SSP using trestle author.

`trestle author ssp-generate` and `trestle author ssp-author` allow users to generate first a set of markdown documents to allow easy editing of control responses and second to reassemble that information up into an OSCAL ssp document. [This is a 'baseline' demonstration](./ssp_author_demo) with more sophisticated updates expected in the near term.

## Trestle repository api (`trestle.core.repository`)

`trestle.core.repository` is an API which abstracts users from the file system of a trestle repository. It provides a way for external developers to access a trestle repository without relying on presumptions (such as cwd being within the repository). Find the demo [here](./trestle_repo_api_examples).

## Task Examples

*Convert a spreadsheet into a `component-definition`*

This [demonstration](./trestle_task_spread_sheet_to_component_definition) shows how to use the `trestle task xlsx-to-oscal-cd` functionality.

*Convert an `xccdf` results into a partial `assessment-results`*

This [demonstration](./trestle_task_xccdf_result_to_oscal_ar) shows how to use the `trestle task xccdf_result_to_oscal_ar` functionality.

## Trestle as Foundation Examples

*Convert Kubernetes results into partial OSCAL `assessment-results`*

Visit external site [Kubernetes WG Policy: OSCAL transformer](https://github.com/kubernetes-sigs/wg-policy-prototypes/tree/master/policy-report/oscal-transformer) for a demo of using `trestle` functionality to create a Kubernetes results (YAML) to OSCAL (JSON) transformer.

## License & Authors

If you would like to see the detailed LICENSE click [here](LICENSE).
Consult [contributors](https://github.com/oscal-compass/compliance-trestle-demos/graphs/contributors) for a list of authors and [maintainers](MAINTAINERS.md) for the core team.

```text
# Copyright (c) 2024 The OSCAL Compass Authors. All rights reserved.
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

```

______________________________________________________________________

We are a Cloud Native Computing Foundation sandbox project.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://www.cncf.io/wp-content/uploads/2022/07/cncf-white-logo.svg">
  <img src="https://www.cncf.io/wp-content/uploads/2022/07/cncf-color-bg.svg" width=300 />
</picture>

The Linux Foundation® (TLF) has registered trademarks and uses trademarks. For a list of TLF trademarks, see [Trademark Usage](https://www.linuxfoundation.org/legal/trademark-usage)".

*Trestle demo's was originally created by IBM.*
