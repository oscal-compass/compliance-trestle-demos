# compliance-trestle-task-osco-to-oscal-demo

Simple example of using trestle to facilitate transforming OSCO results to OSCAL (partial) results.

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
> cd git/compliance-trestle-demos/trestle_task_osco_to_oscal
> trestle init
> trestle task osco-result-to-oscal-ar -c ./demo-osco-to-oscal.config

output: osco/runtime/ssg-ocp4-ds-cis-111.222.333.444-pod.oscal.json
inventory: 1
observations: 125
results: {}
Task: osco-to-oscal executed successfully.
```

Viewing the result

```
> cat osco/runtime/ssg-ocp4-ds-cis-111.222.333.444-pod.oscal.json
{
  "results": [
    {
      "uuid": "d86fdc41-885a-419b-a4f3-1cd3e98167bc",
      "title": "OpenShift Compliance Operator",
      "description": "OpenShift Compliance Operator Scan Results",
      "start": "2022-04-28T02:44:41+00:00",
      "end": "2022-04-28T02:44:41+00:00",
      "props": [
        {
          "name": "scanner_name",
          "ns": "https://ibm.github.io/compliance-trestle/schemas/oscal/ar/osco",
          "value": "OpenSCAP"
        },
        {
          "name": "scanner_version",
          "ns": "https://ibm.github.io/compliance-trestle/schemas/oscal/ar/osco",
          "value": "1.3.3"
        },
    ...
```
