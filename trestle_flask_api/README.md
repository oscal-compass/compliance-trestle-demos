# compliance-trestle-flask-demo

Simple example of using trestle to facilitate building a flask API. It exposes one post endpoint for a catalog at `http://SERVER:PORT/oscal/catalog`. This endpoint will return the payload provided, if valid, and nicely formatted.

This demo is a work in progress and will be expanded as appropriate.

## Running the demo

Use `make develop` to install the appropriate packages into your environment.

Test locally by running `make serve` which will expose the server at `http://127.0.0.1:5000` if allowed by firewalls.
