# k8s-to-oscal

*k8s-to-oscal.py* is a [trestle](https://github.com/IBM/compliance-trestle) based transformer from [Kubernetes YAML](https://github.com/kubernetes-sigs/wg-policy-prototypes) to [OSCAL JSON](https://pages.nist.gov/OSCAL/reference/latest/assessment-results/json-outline/).

This demo showcases using *k8s-to-oscal.py* (built utilizing trestle functionality) to consume YAML results files and produce (partial) OSCAL assessment results.

A [spreadsheet](https://github.com/IBM/compliance-trestle-demos/trestle_k8s/Kubernetes-Yaml-to-OSCAL-Mapping.xlsx) shows the mapping from YAML to OSCAL.

Sample inputs can be found [here](https://github.com/kubernetes-sigs/wg-policy-prototypes/tree/master/policy-report/samples). Sample outputs can be found [here](https://github.com/IBM/compliance-trestle-demos/trestle_k8s/oscal-samples).

#### Demo

![image](images/k8s-to-oscal.drawio.png)

Download this repo.

```
> cd
> mkdir git
> cd git
> git clone https://github.com/IBM/compliance-trestle-demos
```

Install the demo dependencies, ideally in a python virtual environment.

```
> cd
> python -m venv venv.compliance-trestle-demos
> source venv.compliance-trestle-demos/bin/activate
> cd git/compliance-trestle-demos
> make install
```

Run the k8s-to-oscal demo, including fetching the sample YAMLs and invoking the trestle-based transformer to create the corresponding JSONs in OSCAL format.

```
> cd
> cd git/compliance-trestle-demos/trestle_k8s
> make

2022/02/19 08:19:28 I created: sample-cis-k8s.json
2022/02/19 08:19:28 I created: sample-co.json
2022/02/19 08:19:28 I created: sample-falco-policy.json
2022/02/19 08:19:28 I created: sample-rhacm-policy.json
```

List the output files.

```
> ls oscal
sample-cis-k8s.json  sample-co.json  sample-falco-policy.json  sample-rhacm-policy.json
```

