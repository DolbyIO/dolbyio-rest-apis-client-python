# Dolby.io REST APIs Client for Python

Python wrapper for the dolby.io REST [Communications](https://docs.dolby.io/communications-apis/reference/authentication-api), [Streaming](https://docs.dolby.io/streaming-apis/reference) and [Media](https://docs.dolby.io/media-processing/reference/media-enhance-overview) APIs.

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

You can change the log level by using the Python [logging](https://docs.python.org/3/library/logging.html) library.

```python
import logging

logging.basicConfig(level='DEBUG')
```

## Authentication

In order to make API calls for most operations of the **Communications APIs** and **Media APIs**, you must get an access token using this API:

```python
import asyncio
from dolbyio_rest_apis import authentication

APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'

loop = asyncio.get_event_loop()

task = authentication.get_api_token(APP_KEY, APP_SECRET)
at = loop.run_until_complete(task)

print(f'API Token: {at.access_token}')
```

To request a particular scope for this access token:

```python
task = authentication.get_api_token(APP_KEY, APP_SECRET, scope=['comms:*'])
at = loop.run_until_complete(task)

print(f'API Token: {at.access_token}')
print(f'Scope: {at.scope}')
```

## Communications Examples

### Get a client access token

To get an access token that will be used by the client SDK for an end user to open a session against dolby.io, use the following code:

```python
import asyncio
from dolbyio_rest_apis import authentication as auth
from dolbyio_rest_apis.communications import authentication

APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'

loop = asyncio.get_event_loop()

# Request an API Token
task = auth.get_api_token(APP_KEY, APP_SECRET, scope=['comms:client_access_token:create'])
api_token = loop.run_until_complete(task)

print(f'API Token: {api_token.access_token}')

# Request the Client Access Token
task = authentication.get_client_access_token_v2(api_token.access_token, ['*'])
cat = loop.run_until_complete(task)

print(f'Client Access Token: {cat.access_token}')
```

Because most of the APIs are asynchronous, you can write an async function like that:

```python
from dolbyio_rest_apis import authentication as auth
from dolbyio_rest_apis.communications import authentication

APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'

async def get_client_access_token():
    # Request an API Token
    api_token = await auth.get_api_token(APP_KEY, APP_SECRET, scope=['comms:client_access_token:create'])

    # Request the Client Access Token
    cat = await authentication.get_client_access_token_v2(api_token.access_token, ['*'])
    print(f'Client Access Token: {cat.access_token}')
    
    return cat.access_token

```

### Create a conference

To create a Dolby Voice conference, you first must retrieve an API Access Token, then use the following code to create the conference.

```python
import asyncio
from dolbyio_rest_apis import authentication
from dolbyio_rest_apis.communications import conference
from dolbyio_rest_apis.communications.models import Participant, Permission, VideoCodec

APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'

owner_id = '' # Identifier of the owner of the conference
alias = '' # Conference alias

participants = [
    Participant('hostA', [Permission.JOIN, Permission.SEND_AUDIO, Permission.SEND_VIDEO], notify=True),
    Participant('listener1', [Permission.JOIN], notify=False),
]

loop = asyncio.get_event_loop()

# Request an API token
task = authentication.get_api_token(APP_KEY, APP_SECRET, scope=['comms:conf:create'])
at = loop.run_until_complete(task)

# Create the conference
task = conference.create_conference(
    at.access_token,
    owner_id,
    alias,
    video_codec=VideoCodec.VP8,
    participants=participants
)
conf = loop.run_until_complete(task)

print(f'Conference created: {conf.id}')
```

## Real-time Streaming Examples

### Create a publish token

```python
import asyncio
from dolbyio_rest_apis.streaming import publish_token
from dolbyio_rest_apis.streaming.models.publish_token import CreatePublishToken, CreateUpdatePublishTokenStream

API_SECRET = '' # Retrieve your API Secret from the dashboard

create_token = CreatePublishToken('my_token')
create_token.streams.append(CreateUpdatePublishTokenStream('feed1', False))

loop = asyncio.get_event_loop()

task = publish_token.create(API_SECRET, create_token)
token = loop.run_until_complete(task)

print(token)
```

### Create a subscribe token

```python
import asyncio
from dolbyio_rest_apis.streaming import subscribe_token
from dolbyio_rest_apis.streaming.models.subscribe_token import CreateSubscribeToken, CreateUpdateSubscribeTokenStream

API_SECRET = '' # Retrieve your API Secret from the dashboard

create_token = CreateSubscribeToken('my_token')
create_token.streams.append(CreateUpdateSubscribeTokenStream('feed1', False))

loop = asyncio.get_event_loop()

task = publish_token.create(API_SECRET, create_token)
token = loop.run_until_complete(task)

print(token)
```

## Media Examples

Here is an example on how to upload a file to the Dolby.io temporary cloud storage, enhance that file and download the result.

### Get an API token

Get the App Key and Secret from the Dolby.io dashboard and use the following code in your python script.

```python
import asyncio
from dolbyio_rest_apis import authentication

APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'

loop = asyncio.get_event_loop()

task = authentication.get_api_token(APP_KEY, APP_SECRET, 2 * 60 * 60) # 2 hours
at = loop.run_until_complete(task)
print(f'API token: {at.access_token}')
```

### Upload a file for processing

Add the following `import` to your script.

```python
from dolbyio_rest_apis.media import io
```

Using the API token, start by requesting an upload URL.

```python
# Temporary storage URL that will be used as reference for the job processing
input_url = 'dlb://in/file.mp4'

# Get an Upload URL
task = io.get_upload_url(
    access_token=at.access_token,
    dlb_url=input_url,
)
upload_url = loop.run_until_complete(task)
print(f'Upload URL: {upload_url}')
```

Upload a media file to the Dolby.io temporary cloud storage for processing:

```python
# Location of the original file on the local machine
IN_FILE_PATH = '/path/to/original_file.mp4'

# Upload the file
task = io.upload_file(
    upload_url=upload_url,
    file_path=IN_FILE_PATH,
)
loop.run_until_complete(task)
```

### Start an enhance job

Add the following `import` to your script.

```python
import json
from dolbyio_rest_apis.media import enhance
```

Generate a job description and send it to Dolby.io.

```python
# Temporary storage URL where the service will write the result file to
output_url = 'dlb://out/file.mp4'

# Job description
job = {
    'input': input_url,
    'output': output_url,
    'content': {
        'type': 'podcast',
    },
}
job_str = json.dumps(job, indent=4)
print(job_str)

# Start the enhance job and get a job ID back
task = enhance.start(at.access_token, job_str)
job_id = loop.run_until_complete(task)
print(f'Job ID: {job_id}')
```

### Wait for the job to complete

Add the following `import` to your script.

```python
import sys
import time
```

Get the job status and wait until it is completed.

```python
task = enhance.get_results(at.access_token, job_id)
result = loop.run_until_complete(task)
while result.status in ( 'Pending', 'Running' ):
    print(f'Job status is {result.status}, taking a 5 second break...')
    time.sleep(5)

    task = enhance.get_results(at.access_token, job_id)
    result = loop.run_until_complete(task)

if result.status != 'Success':
    print('There was a problem with processing the file')
    print(json.dumps(result, indent=4))
    sys.exit(1)
```

### Download a processed file

At this stage, the file has been processed and written to the temporary storage so we can download it.

```python
# Where to download the file on the local machine
OUT_FILE_PATH = '/path/to/processed_file.mp4'

task = io.download_file(
    access_token=at.access_token,
    dlb_url=output_url,
    file_path=OUT_FILE_PATH,
)
loop.run_until_complete(task)
```
