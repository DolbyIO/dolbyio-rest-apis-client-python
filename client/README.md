# Dolby.io REST APIs

Python wrapper for the dolby.io REST [Communications](https://docs.dolby.io/communications-apis/reference/authentication-api) and [Media](https://docs.dolby.io/media-processing/reference/media-enhance-overview) APIs. All the functions are using the async pattern.

## Install this project

Check the [dolbyio-rest-apis](https://pypi.org/project/dolbyio-rest-apis/) package on PyPI. To install the latest stable python package run the following command: 

```bash
python3 -m pip install dolbyio-rest-apis
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

APP_KEY = "YOUR_APP_KEY"
APP_SECRET = "YOUR_APP_SECRET"

loop = asyncio.get_event_loop()
task = authentication.get_api_token(APP_KEY, APP_SECRET)
at = loop.run_until_complete(task)

print(f"Access Token: {at.access_token}")
```

You can write an async function like that:

```python
from dolbyio_rest_apis.communications import authentication

APP_KEY = "YOUR_APP_KEY"
APP_SECRET = "YOUR_APP_SECRET"

async def get_client_access_token():
    at = await authentication.get_client_access_token(APP_KEY, APP_SECRET)
    print(f"Access Token: {at.access_token}")

```

To get an access token that will be used by your server to perform backend operations like creating a conference, use the following code.

```python
import asyncio
from dolbyio_rest_apis.communications import authentication

APP_KEY = "YOUR_APP_KEY"
APP_SECRET = "YOUR_APP_SECRET"

loop = asyncio.get_event_loop()
task = authentication.get_api_access_token(APP_KEY, APP_SECRET)
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

## Media Examples

### Media Input and Output

Upload a media file to the temporary Dolby.io cloud storage for processing:

```python
import asyncio
from dolbyio_rest_apis.media import io

ACCESS_TOKEN = "YOUR_API_TOKEN"

# Get an Upload URL
task = io.get_upload_url(
    access_token=ACCESS_TOKEN,
    dlb_url='dlb://in/file.mp4'
)
upload_url = loop.run_until_complete(task)

print(f"Upload URL: {upload_url}")

# Upload the file
task = io.upload_file(
    upload_url=upload_url,
    file_path='/path/to/file.mp4'
)
loop.run_until_complete(task)
```

Download a file that was processed by the API:

```python
import asyncio
from dolbyio_rest_apis.media import io

ACCESS_TOKEN = "YOUR_API_TOKEN"

task = io.download_file(
    access_token=ACCESS_TOKEN,
    dlb_url='dlb://out/file.mp4',
    file_path='/path/to/processed_file.mp4'
)
loop.run_until_complete(task)
```
