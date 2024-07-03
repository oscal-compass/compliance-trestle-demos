# Trestle SDK examples

A container for a set of simpler examples of using the trestle SDK.

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
> cd trestle_sdk_examples
> python create_a_catalog.py
```

Running `python create_a_catalog.py` will first try and fail to create a catalog (by failing to provide required attributes), then create a catalog, followed by writing it out to disk.
