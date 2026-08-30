# compliance-trestle-task-xlsx-to-oscal-poam-demo

Simple example of using trestle to facilitate building an OSCAL POAM from a spread sheet (.xlsx)

## Prerequisites

Download this repo

```
> cd
> mkdir git
> cd git
> git clone https://github.com/oscal-compass/compliance-trestle-demos
> cd compliance-trestle-demos
```

### demo: trestle task xlsx-to-oscal-poam

This demo transforms the .xlsx to OSCAL POAM.

```
> cd trestle_task_cis_xlsx_to_oscal_cd
> make
source /home/degenaro/venv-set/venv.poam/bin/activate; \
mkdir -p trestle.ws; \
cd trestle.ws; \
trestle init;

Initialized trestle project successfully in /home/degenaro/git/compliance-trestle-demos.poam/trestle_task_xlsx_to_oscal_poam/trestle.ws
echo "=> create POAM from .xlsx"; \
source /home/degenaro/venv-set/venv.poam/bin/activate; \
cd trestle.ws; \
trestle task xlsx-to-oscal-poam --config ../demo-xlsx-to-oscal-poam.config

=> create POAM from .xlsx
Created POAM with 6 items
Output: plan-of-action-and-milestones/FedRAMP/plan-of-action-and-milestones.json
Task: xlsx-to-oscal-poam executed successfully.
```

Display POAM

```
> cat trestle.ws/plan-of-action-and-milestones/FedRAMP/plan-of-action-and-milestones.json 
{
  "plan-of-action-and-milestones": {
    "uuid": "43a9120e-a190-404c-b5f7-cfb758804cf8",
    "metadata": {
      "title": "FedRAMP",
      "last-modified": "2026-06-18T18:56:37+00:00",
      "version": "1.0",
      "oscal-version": "1.2.1"
    },
    "observations": [
      {
        "uuid": "2f498fdd-8751-51c4-a3d5-a97aa1a3dee6",
        "description": "Weakness detected: Outdated Linux Kernel Vulnerability (CVE-2024-1086)",
        "methods": [
          "TEST"
        ],
...
```