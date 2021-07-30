# ssp_author_demo

This demonstration of \[compliance-trestle\]((https://ibm.github.io/compliance-trestle) is designed to show how `trestle author` can be used to enable version controlled editing of SSP responses.

The trestle project has been setup with a catalog and profile from NIST using 800-53. This was used to generate the markdown directory.

SSP generate is used to generate the markdown files based on the combination of a profile and a single catalog. [Multi-stage profile resolution](https://github.com/IBM/compliance-trestle/issues/648) is a work in progress.

The pro

## Steps to recreate setup

### Initial import

- trestle init was run
- The [OSCAL-content](https://github.com/usnistgov/OSCAL-content) repository was cloned.
- The [NIST 800-53 catalog](https://github.com/usnistgov/oscal-content/blob/master/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json) was imported with `trestle import -f {path to catalog} -o 800-53`
  - The catalog will be inserted within `./catalogs/800-53/`
- The [NIST 800-53 LOW profile](https://github.com/usnistgov/oscal-content/blob/master/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline_profile.json) was imported with trestle import -f {path to profile} -o 800-53-low\`
  - The profiles will be inserted within `./profiles/800-53-low/`
- The profile is updated such that it refers to the catalog by the catalog name (e.g. `800-53.json`) [note see upcoming changes](https://github.com/IBM/compliance-trestle/issues/557)

### Inserting parameters

Profiles from NIST do not insert parameter values by default so the profile needs to be modified.

- `cd ./profiles/800-53-low/`
- Add the missing modify structure`trestle add -f ./profile.json -e 'profile.modify'`
- Create some sample parameters: `trestle add -f ./profile.json -e 'profile.modify.set-parameters'`
- The parameters now need to be set by using the `value` field. For this demo all the parameters for ac-1 have been set.

### Populating response content

- First the response documents must be generated using:
  - cd to the project root directory
  - `trestle author ssp-generate -p 800-53-low --output test_system -s 'guidance:Control Guidance'`
  - `--output` puts the markdown directory tree into `./test_system`
  - `-s` maps named parts names to sections in catalog to the markdown document
- Content is edited by end users (in this case ac-1 part a)

### Creating the OSCAL catalog

- Run
  - `trestle author ssp-assemble -m test_system -o acme-test-system`
- The ssp will be generated in `./system-security-plans/acme-test-system`
