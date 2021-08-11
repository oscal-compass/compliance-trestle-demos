# Trestle Respository API examples

This demo shows examples of using the trestle repository APIs for accessing and manipulating the repository objects programmatically.

## Running the demo

A trestle workspace (repository) has been initialized in .`/trestle-workspace` directory.

The `repo-examples.py` will first create a Repository object by passing the trestle workspace as input and then read the included NIST 800-53 catalog json file into a catalog object, then import it into repository and perform various operations on it using the repository API.

To run the demo, execute the folloiwng command:

```
python3 repo-examples.py
```
