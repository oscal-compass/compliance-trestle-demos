# ssp_author_demo

This demonstration of [compliance-trestle](https://ibm.github.io/compliance-trestle) is designed to show how `trestle author` can be used to generate System-Security-Plan(SSP) markdown files from its OSCAL profile and its imported catalogs and profiles, and vice versa.

This demo requires trestle version 3.x.x

## Steps

### Download this repo

```
> cd
> mkdir git
> cd git
> git clone https://github.com/oscal-compass/compliance-trestle-demos.git
```

### Install compliance trestle, ideally in a python virtual environment, and create a trestle workspace

```
> cd
> python -m venv venv.compliance-trestle-demos
> source venv.compliance-trestle-demos/bin/activate
> cd git/compliance-trestle-demos
> make install
> cd ssp_author_demo
> trestle init
```

### Download example catalog([NIST 800-53 catalog](https://github.com/usnistgov/oscal-content/blob/master/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json)) and profile([NIST 800-53 LOW profile](https://github.com/usnistgov/oscal-content/blob/master/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline_profile.json))

```
> cd
> git clone https://github.com/usnistgov/OSCAL-content
> cd git/compliance-trestle-demos/ssp_author_demo
> trestle import -f ~/OSCAL-content/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json -o 800-53
> trestle import -f ~/OSCAL-content/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline_profile.json -o 800-53-low
```

The example catalog and profile are inserted within `./catalogs/800-53/` and `./profiles/800-53-low/`.\
Note, the `url` in the example profile doesn't correctly link to the imported catalog.
Select the imported profile, and scroll down to the `resources` section and replace the json media-type's `href` value to: `trestle://catalogs/800-53/catalog.json`

### Inserting parameters

Profiles from NIST do not insert parameter values by default, so the profile needs to be modified.

- `cd ./profiles/800-53-low/`
- Add the missing modify structure`trestle create -f ./profile.json -e 'profile.modify'`
- Create some sample parameters: `trestle create -f ./profile.json -e 'profile.modify.set-parameters'`

### Generating SSP markdown files

- First the response documents must be generated using:
  - `cd ~/git/compliance-trestle-demos/ssp_author_demo` to demo root directory.
  - `trestle author ssp-generate -p 800-53-low --output test_system`
  - `--output` puts the markdown directory tree into `./test_system`
- Content for the implemented requirements can now be entered into the markdown for controls

### Convert SSP markdown files to OSCAL

- Run
  - `trestle author ssp-assemble -m test_system -o acme-test-system`
- The SSP will be generated in `./system-security-plans/acme-test-system`
- The generated json OSCAL document will be a valid system-security-plan with the implemented requirements incorporated for the controls.
- The requirements are provided "by component" and in this demo there is only one default component: "This System".  In general
  there can be more than one component.
