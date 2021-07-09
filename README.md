# compliance-trestle-demos

A project capturing a number of demos and sample sets of cotnent for the [compliance-trestle](https://ibm.github.io/compliance-trestle) project including various additional scripts and transformers.

## Using / management of this repository

This project follows the same methodologies as within the main trestle project in terms of [contributing and developer setup](https://ibm.github.io/compliance-trestle/contributing/mkdocs_contributing/). Please submit [issues here](https://github.com/IBM/compliance-trestle/issues/new/choose) relating to this project.

The top level project itself is a container for a set of demonstrations. At a high level all files are expected to pass:

- mdformat setup
- code-linting for python files
- code-formatting for python files.

All content provided here is 'as is' and is not required to pass unit testing etc.

To add a demonstration in addition to opening a PR with the new demonstration in a single folder within the top level project:

- The demonstration folder must have it's own [README.md](ISM_catalog_profile/README.md)
- The list of demonstrations in this folder must be updated.
- A PR must be opened to update

### Demos with CICD

- Some of the demonstrations may integrate with CICD systems (e.g. travis / github actions / circle CI)
- To simplify this project those demonstrations

# Demonstrations

## Australian government Information Security Manual (ISM)

This demonstration uses trestle as an SDK for generating OSCAL files.
A script `scripts/ISM/ISM.py` generates a set of profiles (for each security level) and a catalog per ISM version.
Read more about the demo [here](./scripts/ISM/ISM.py).

## arc42 architectural template enforcement using trestle author.

[arc42](https://arc42.org/) have created a set open-source architecture documentation templates. This [demonstration](./arc42-author-demo)
uses `trestle author` to enforce use of the (modified) arc42 templates.

A CICD pipeline (using github actions) is used for this demonstration. The full repository, including working CICD is [here](https://github.com/IBM/compliance-trestle-arc42-demo). Read more about the demo [here](https://github.com/IBM/compliance-trestle-arc42-demo)

## License & Authors

If you would like to see the detailed LICENSE click [here](LICENSE).
Consult [contributors](https://github.com/IBM/compliance-trestle/graphs/contributors) for a list of authors and [maintainers](MAINTAINERS.md) for the core team.

Note that some content referenced within this repository is under separate licenses and is annotated as such.

```text
# Copyight (c) 2021 IBM Corp. All rights reserved.
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
```
