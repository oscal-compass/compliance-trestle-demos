# ssp_author_demo

This demonstration of \[compliance-trestle\]((https://ibm.github.io/compliance-trestle) is designed to show how `trestle author` can be used to enable version controlled editing of SSP responses.

The trestle project has been setup with a catalog and profile from NIST using 800-53. This was used to generate the markdown directory.

SSP generate is used to generate the markdown files from a profile and its imported catalogs and profiles.  Prompts are provided in the markdown for
each control where an implementation response is required, corresponding to parts in the control statement.

This demo requires trestle version 1.0.x

## Steps to recreate setup

### Initial import

- trestle init was run
- The [OSCAL-content](https://github.com/usnistgov/OSCAL-content) repository was cloned.
- The [NIST 800-53 catalog](https://github.com/usnistgov/oscal-content/blob/master/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json) was imported with `trestle import -f {path to catalog} -o 800-53`
  - The catalog will be inserted within `./catalogs/800-53/`
- The [NIST 800-53 LOW profile](https://github.com/usnistgov/oscal-content/blob/master/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline_profile.json) was imported with trestle import -f {path to profile} -o 800-53-low\`
  - The profiles will be inserted within `./profiles/800-53-low/`
- The profile is updated so the import href points within the trestle project to `trestle://catalogs/800-53/catalog.json`

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
- Content for the implemented requirements can now be entered into the markdown for controls

### Creating the OSCAL catalog

- Run
  - `trestle author ssp-assemble -m test_system -o acme-test-system`
- The ssp will be generated in `./system-security-plans/acme-test-system`
- The generated json OSCAL document will be a valid system-security-plan with the implemented requirements incorporated for the controls.
- The requirements are provided "by componenent" and in this demo there is only one default component: "This System".  In general
  there can be more than one component.
