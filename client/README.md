# Dolby.io REST APIs

Python wrapper for the dolby.io REST APIs [Communications](https://docs.dolby.io/communications-apis/reference/authentication-api). All the functions are using the async pattern.

## Install this project

Check the [dolbyio-rest-apis](https://pypi.org/project/dolbyio-rest-apis/) package on PyPI. To install the latest stable python package run the following command: 

```bash
python3 -m pip install  dolbyio-rest-apis
```

Upgrade your package to the latest version:

```bash
python3 -m pip install --upgrade dolbyio-rest-apis
```

## Logging

You can change the log level by using the Python (logging)[https://docs.python.org/3/library/logging.html] library.

```python
import logging

logging.basicConfig(level="DEBUG")
```

## Communications Examples

### Authenticate

To get an access token that will be used by the client SDK for an end user to open a session against dolby.io, use the following code:

```python
import asyncio
from dolbyio_rest_apis.communications import authentication

CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"

loop = asyncio.get_event_loop()
task = authentication.get_client_access_token(CONSUMER_KEY, CONSUMER_SECRET)
at = loop.run_until_complete(task)

print(f"Access Token: {at.access_token}")
```

You can write an async function like that:

```python
from dolbyio_rest_apis.communications import authentication

CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"

async def get_client_access_token():
    at = await authentication.get_client_access_token(CONSUMER_KEY, CONSUMER_SECRET)
    print(f"Access Token: {at.access_token}")

```

To get an access token that will be used by your server to perform backend operations like creating a conference, use the following code.

```python
import asyncio
from dolbyio_rest_apis.communications import authentication

CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"

loop = asyncio.get_event_loop()
task = authentication.get_api_access_token(CONSUMER_KEY, CONSUMER_SECRET)
at = loop.run_until_complete(task)

print(f"Access Token: {at.access_token}")
```

### Create a conference

To create a Dolby Voice conference, you first must retrieve an API Access Token, then use the following code to create the conference.

```python
import asyncio
from dolbyio_rest_apis.communications import conference
from dolbyio_rest_apis.communications.models import Participant, Permission, VideoCodec

access_token = "" # Retrieve an API Access Token
owner_id = "" # Identifier of the owner of the conference
alias = "" # Conference alias

participants = [
    Participant("hostA", [Permission.JOIN, Permission.SEND_AUDIO, Permission.SEND_VIDEO], notify=True),
    Participant("listener1", [Permission.JOIN], notify=False),
]

loop = asyncio.get_event_loop()
task = conference.create_conference(
    access_token,
    owner_id,
    alias,
    video_codec=VideoCodec.VP8,
    participants=participants
)
conf = loop.run_until_complete(task)

print(f"Conference created: {conf.id}")
```
