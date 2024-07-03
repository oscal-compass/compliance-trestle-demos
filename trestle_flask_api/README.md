# compliance-trestle-flask-demo

Simple example of using trestle to facilitate building a flask API. It exposes one post endpoint for a catalog at `http://SERVER:PORT/oscal/catalog`. This endpoint will return the payload provided, if valid, and nicely formatted.

This demo is a work in progress and will be expanded as appropriate.

This demo requires trestle version 3.x.x

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

Use `make develop` to install the appropriate packages into your environment.\
Test locally by running `make serve` which will expose the server at `http://127.0.0.1:5000` if allowed by firewalls.

```
> cd trestle_flask_api
> make develop
> make serve
```

Now, the server is ready to accept a `POST` request at endpoint `http://127.0.0.1:5000/oscal/catalog` with `Catelog` in the request body.

```
> curl --location 'http://127.0.0.1:5000/oscal/catalog' \
--header 'Content-Type: application/json' \
--data '{
    "uuid": "7e54b37f-d7b8-4f8f-901b-cd0983c1feb1",
    "metadata": {
        "title": "my cool catalog",
        "last-modified": "2024-06-26T14:54:14.089987-04:00",
        "version": "0.0.1",
        "oscal-version": "1.0.0"
    }
}'
```

The expected output should be the following:

```
{
  "title": "my cool catalog",
  "last-modified": "2024-06-26T18:54:14.089+00:00",
  "version": "0.0.1",
  "oscal-version": "1.0.0"
}
```
