# Dolby.io REST APIs CLI

Command Line Interface utility for the dolby.io REST [Communications](https://docs.dolby.io/communications-apis/reference/authentication-api) APIs.

## Install this project

Check the [dolbyio-rest-apis-cli](https://pypi.org/project/dolbyio-rest-apis-cli/) package on PyPI. To install the latest stable python package run the following command: 

```bash
python3 -m pip install dolbyio-rest-apis-cli
```

Upgrade your package to the latest version:

```bash
python3 -m pip install --upgrade dolbyio-rest-apis-cli
```

## Communications Commands

Display the help and version of the command line:

```bash
communications --help
communications --version
```

### Authentication

Get your consumer key and secret from the dolby.io dashboard and run the following command to get the access token as a json payload:

```bash
communications auth -k "CONSUMER_KEY" -s "CONSUMER_SECRET" --output json
```

Add the flag `--api` to get an access token that you can use to query the REST APIs.  
Change the output to `--output text` to get a text format for the output.  
Use `--output access_token` to retrieve only the access token so you can easily assign it to a variable:

```bash
ACCESS_TOKEN=$(communications auth -k "CONSUMER_KEY" -s "CONSUMER_SECRET" --api --output access_token 2> /dev/null)
```

### Remix

Using the access token you've retrieved using the `auth` command, you can start a remix for a specific conference:

```bash
communications remix \
    --access_token "ACCESS_TOKEN" \
    --cid "00000000-0000-0000-0000-000000000000" \
    --start \
    --output json
```

Or simply check the status of a remix:

```bash
communications remix \
    --access_token "ACCESS_TOKEN" \
    --cid "00000000-0000-0000-0000-000000000000" \
    --output json
```

### Streaming

Start the streaming to an RTMP endpoint for a specific conference:

```bash
communications streaming \
    --access_token "ACCESS_TOKEN" \
    --cid "00000000-0000-0000-0000-000000000000" \
    --action start \
    --target rtmp \
    --output json \
    --urls "rtmp://a.rtmp.youtube.com/live2/{streaming_key}"
```

Stop the RTMP streaming for a specific conference:

```bash
communications streaming \
    --access_token "ACCESS_TOKEN" \
    --cid "00000000-0000-0000-0000-000000000000" \
    --action stop \
    --target rtmp \
    --output json
```
