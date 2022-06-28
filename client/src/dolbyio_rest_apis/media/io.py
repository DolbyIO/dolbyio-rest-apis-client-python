"""
dolbyio_rest_apis.media.io
~~~~~~~~~~~~~~~

This module contains the functions to work with the IO APIs.
"""

from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext

async def get_upload_url(
        access_token: str,
        dlb_url: str,
    ) -> str or None:
    r"""
    Start Media Input

    To use the Dolby provided temporary storage is a two step process.

    You start by declaring a dlb:// url that you can reference in any other Media API calls.
    The response will provide a url where you can put your media.
    This allows you to use the dlb:// url as a short-cut for a temporary storage location.

    You'll be returned a pre-signed url you can use to PUT and upload your media file.
    The temporary storage should allow you to read and write to the dlb:// locations for a period of at least 24 hours before it is removed.

    See: https://docs.dolby.io/media-apis/reference/media-input-post

    Args:
        access_token: Access token to use for authentication.
        dlb_url: The `url` should be in the form `dlb://object-key` where the object-key can be any alpha-numeric string.
            The object-key is unique to your account API Key so there is no risk of collision with other users.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    payload = {
        'url': dlb_url
    }

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url='https://api.dolby.com/media/input',
            payload=payload
        )

    if 'url' in json_response:
        return json_response['url']

async def upload_file(
        upload_url: str,
        file_path: str,
    ) -> None:
    r"""
    Upload a file.

    Args:
        upload_url: URL where to upload the file to.
        file_path: Local file path to upload.

    Raises:
        HTTPError: If one occurred.
    """
    async with MediaHttpContext() as http_context:
        await http_context.upload(
            upload_url=upload_url,
            file_path=file_path,
        )

async def download_file(
        access_token: str,
        dlb_url: str,
        file_path: str,
    ) -> None:
    r"""
    Start Media Download

    You can download media you previously uploaded with /media/input or media that was generated through another Dolby Media API.

    The temporary storage should allow you to read and write to the dlb:// locations for a period of at least 24 hours before it is removed.

    See: https://docs.dolby.io/media-apis/reference/media-output-get

    Args:
        access_token: Access token to use for authentication.
        dlb_url: The `url` should be in the form `dlb://object-key` where the object-key can be any alpha-numeric string.
            The object-key is unique to your account API Key so there is no risk of collision with other users.
        file_path: Local file path where to download the file to.

    Raises:
        HTTPError: If one occurred.
    """
    params = {
        'url': dlb_url,
    }

    async with MediaHttpContext() as http_context:
        await http_context.download(
            access_token=access_token,
            url='https://api.dolby.com/media/output',
            file_path=file_path,
            params=params,
        )
