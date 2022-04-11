# Dolby.io REST APIs

This repo contains projects for the dolby.io REST [Communications](https://docs.dolby.io/communications-apis/reference/authentication-api) and [Media](https://docs.dolby.io/media-processing/reference/media-enhance-overview) APIs.
- Command Line Interface utility.

## Build the builder

Install the package dependencies to build the installers:

```bash
python3 -m pip install -r requirements.txt
```

## Build the client project

Install the package dependencies to build and run this project:

```bash
python3 -m pip install -r client/requirements.txt
```

Build this project wheel:

```bash
python3 client/setup.py sdist bdist_wheel
```

## Build the CLI project

Install the package dependencies to build and run this project:

```bash
python3 -m pip install -r cli/requirements.txt
```

Build this project wheel:

```bash
python3 cli/setup.py sdist bdist_wheel
```

## Run PyLint on the code

Run the following [pylint](https://pylint.org/) command:

```bash
python3 -m pylint \
    client/src/dolbyio_rest_apis \
    cli/src/dolbyio_rest_apis_cli
```
