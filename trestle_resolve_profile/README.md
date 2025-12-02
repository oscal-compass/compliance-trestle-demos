# Trestle resolve profile example

Use trestle to resolve profile.

## Prerequisites
Download this repo

```
> cd
> mkdir git
> cd git
> git clone https://github.com/oscal-compass/compliance-trestle-demos.git
```

Install compliance trestle, ideally in a python virtual environment.

```
> cd
> python -m venv venv.compliance-trestle-demos
> source venv.compliance-trestle-demos/bin/activate
> cd git/compliance-trestle-demos
> make install
```

## Running the demo
```
> cd trestle_resolve_profile
> trestle init
```

```
> cp -pr ../resources/catalogs/* catalogs
> cp -pr ../resources/profiles/* profiles
```

```
> trestle author profile-resolve --name NIST_800-53_rev5_selected --output NIST_800-53_rev5_selected_resolved
```

```
> trestle validate -a
VALID: Model /home/degenaro/git/demos.resolved-profile/trestle_resolve_profile/catalogs/NIST_800-53_rev5/catalog.json passed the Validator to confirm the model passes all registered validation tests.
VALID: Model /home/degenaro/git/demos.resolved-profile/trestle_resolve_profile/catalogs/NIST_800-53_rev5_selected_resolved/catalog.json passed the Validator to confirm the model passes all registered validation tests.
VALID: Model /home/degenaro/git/demos.resolved-profile/trestle_resolve_profile/profiles/NIST_800-53_rev5_selected/profile.json passed the Validator to confirm the model passes all registered validation tests.
```

```
> cat catalogs/NIST_800-53_rev5_selected_resolved/catalog.json
{
  "catalog": {
    "uuid": "87dcded6-8da7-4cfc-aa6c-37c11ba12f33",
    "metadata": {
      "title": "NIST SP 800-53 Rev 5 Controls, selected",
      "last-modified": "2025-03-29T11:10:44.084066+00:00",
      "version": "0.1.6",
      "oscal-version": "1.1.3",
      "links": [
        {
          "href": "catalogs/NIST_800-53_rev5/catalog.json",
          "rel": "resolution-source"
        }
      ]
    },
    "controls": [
      {
        "id": "ac-1",
        "class": "SP800-53",
        "title": "Policy and Procedures",
        "params": [
          {
            "id": "ac-1_prm_1",
            "props": [
              {
                "name": "aggregates",
                "ns": "http://csrc.nist.gov/ns/rmf",
                "value": "ac-01_odp.01"
              },
              {
                "name": "aggregates",
                "ns": "http://csrc.nist.gov/ns/rmf",
                "value": "ac-01_odp.02"
              }
            ],
            "label": "organization-defined personnel or roles"
          },
          {
            "id": "ac-01_odp.01",
            "props": [
              {
                "name": "label",
                "value": "AC-01_ODP[01]",
                "class": "sp800-53a"
              }
            ],
            "label": "personnel or roles",
            "guidelines": [
              {
                "prose": "personnel or roles to whom the access control policy is to be disseminated is/are defined;"
              }
            ],
            "values": [
              "Test Value"
            ]
          },
...
```
