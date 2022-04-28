# compliance-trestle-task-spread-sheet-to-component-definition-demo

Simple example of using trestle to facilitate building an OSCAL component-definition from a spread sheet (.xlsx) and controls catalog.

## Prerequisites

Download this repo

```
> cd
> mkdir git
> cd git
> git clone https://github.com/IBM/compliance-trestle-demos
```

Install compliance trestle, ideally in a python virtual environment.

```
> cd
> python -m venv venv.compliance-trestle-demos
> source venv.compliance-trestle-demos/bin/activate
> cd git/compliance-trestle-demos
> make install
```

Running the demo

```
> cd
> cd git/compliance-trestle-demos/trestle_task_spread_sheet_to_component_definition
> trestle task xlsx-to-oscal-cd -c ./demo-xlsx-to-component-definition.config

catalog: trestle-workspace/catalogs/nist-sp-800-53-rev4/catalog.json
input: demo.xlsx
row 5 col AS missing value
row 8 control cm-8_3 edited to remove parentheses
row=9 edited source_code_scaning_vulnerability_threashhold to remove whitespace
row 9 control cm-8_3 edited to remove parentheses
row=11 edited source_code_scaning_vulnerability_threashhold to remove whitespace
row 11 control zz-1 not found in catalog
output: trestle-workspace/component-definitions/component-definition.json
rows missing goal_name_id: [2]
rows missing controls: [10]
rows missing parameters: [2, 7, 8]
rows missing parameters values: [5]
output: trestle-workspace/catalogs/catalog.json
Task: xlsx-to-oscal-component-definition executed successfully.
```

Viewing the result

```
> cat trestle-workspace/component-definitions/component-definition.json

{
"component-definition": {
"uuid": "75c68a4b-9395-470d-9653-0ae99c93f558",
"metadata": {
  "title": "Component definition for NIST Special Publication 800-53 Revision 4 profiles",
  "last-modified": "2021-07-28T13:22:19.000+00:00",
  "version": "0.20.0",
  "oscal-version": "1.0.0",
  "roles": [
    {
      "id": "prepared-by",
      "title": "Indicates the organization that created this content."
    },
    ...
```
