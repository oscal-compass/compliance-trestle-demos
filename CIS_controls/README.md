# CIS Controls conversion script

The Centre for Internet Security (CIS) produce a number of cross industry standards for IT security including their [platform specific benchmarks](https://www.cisecurity.org/cis-benchmarks/) and a suite of [controls](https://www.cisecurity.org/controls/). This demo converts a spreadsheet of those controls into a catalog and three profiles.

## Prerequisites

Download the [CIS controls Excel spreadsheet](https://www.cisecurity.org/controls/) to your chosen location.

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
> cd CIS_controls
> python create_cis_catalogs_profiles.py -i path_to_cis_spreadsheet.xlsx -o output_directory_defaults_to_cwd
```

In the chosen output directory 1 catalog and 3 profiles will be created.

## Notes on licensing.

CIS is licensed content and is not open source. This demonstration works with the CIS controls Excel spreadsheet version 8.1 (downloaded as: `CIS Controls Version 8 Final_05-24-2021.xlsx`) Drift from this version may introduce errors. If you have any trouble open an issue [here](https://github.com/IBM/compliance-trestle/issues/new/choose).

## Notes on terminology of CIS vs OSCAL / NIST

NIST's control hierarchy has groups, controls and sub-controls. In this model sub-controls are not fractional elements, however, enhancements in addition to the obligations of the top level controls.

In the CIS control hierarchy there are 'controls' and 'safeguards'. In the way the CIS controls are constructed there is room to debate as to whether it is better to map that two levels of hierarchy to 'groups and controls' or 'controls and sub-controls'.

Given this language difference and the uncertainty we mapped CIS 'controls and safeguards' to OSCAL 'controls and sub-controls' based on the minimization of language differences.
