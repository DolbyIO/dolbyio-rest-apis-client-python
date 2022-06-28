"""
Command: Input / Output
"""

from argparse import _SubParsersAction, Namespace
from dolbyio_rest_apis.media import io

def command_name() -> str:
    return 'io'

def add_arguments(sub_parsers: _SubParsersAction) -> None:
    parser = sub_parsers.add_parser(command_name(), help='Input / Output')

    parser.add_argument(
		'-a', '--access_token',
		help='Your API Access Token.',
		required=True,
		type=str
	)

    parser.add_argument(
		'--dlb_url',
		help='''
        The `url` should be in the form `dlb://object-key` where the object-key can be any alpha-numeric string.
        The object-key is unique to your account API Key so there is no risk of collision with other users.
        ''',
		required=True,
		type=str
	)

    parser.add_argument(
		'--file',
		help='File to upload.',
		required=True,
		type=str
	)

    sub_parsers_io = parser.add_subparsers(dest='sub_command')
    sub_parsers_io.add_parser('upload', help='Upload a file')
    sub_parsers_io.add_parser('download', help='Download a file')

async def execute_command(args: Namespace) -> None:
    access_token = args.access_token
    dlb_url = args.dlb_url
    file = args.file

    if args.sub_command == 'upload':
        upload_url = await io.get_upload_url(
            access_token=access_token,
            dlb_url=dlb_url
        )

        print(f'Upload URL: {upload_url}')

        await io.upload_file(
            upload_url=upload_url,
            file_path=file
        )

        print(f'File uploaded to {dlb_url}')
    elif args.sub_command == 'download':
        await io.download_file(
            access_token=access_token,
            dlb_url=dlb_url,
            file_path=file
        )

        print(f'File saved at {file}')
