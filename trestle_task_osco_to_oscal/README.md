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
> trestle task osco-to-oscal -c ./demo-osco-to-oscal.config

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
      "uuid": "5a69ce39-9ec9-4ded-8556-2c94a5b4e554",
      "title": "OpenShift Compliance Operator",
      "description": "OpenShift Compliance Operator Scan Results",
      "start": "2021-09-09T19:18:09.000+00:00",
      "end": "2021-09-09T19:18:09.000+00:00",
      "local-definitions": {
        "components": [
          {
            "uuid": "1690228d-860d-4fa0-a43b-c95f2f53410e",
            "type": "Service",
            "title": "Red Hat OpenShift Kubernetes Service Compliance Operator for ocp4",
            "description": "Red Hat OpenShift Kubernetes Service Compliance Operator for ocp4",
            "status": {
              "state": "operational"
            }
          }
        ],
        "inventory-items": [
          {
            "uuid": "d4dff670-fe5e-4324-94aa-c1fffdef17c5",
            "description": "inventory",
            "props": [

    ...
```
