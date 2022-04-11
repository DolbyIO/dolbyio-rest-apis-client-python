"""
Command: Authentication
"""

from argparse import _SubParsersAction, Namespace
from dolbyio_rest_apis.media import platform
import json

def command_name() -> str:
    return 'auth'

def add_arguments(sub_parsers: _SubParsersAction) -> None:
    parser = sub_parsers.add_parser(command_name(), help='Authentication')

    parser.add_argument(
		'-k', '--api_key',
		help='Your Dolby.io API Key',
		default='',
		type=str
	)

    parser.add_argument(
		'-s', '--api_secret',
		help='Your Dolby.io API Secret',
		default='',
		type=str
	)

    parser.add_argument(
		'-o', '--output',
		help='Set the output format.',
		dest='output_format',
		default='json',
        choices=[ 'json', 'text', 'access_token' ]
	)

async def execute_command(args: Namespace) -> None:
    api_key = args.api_key
    api_secret = args.api_secret
    output_format = args.output_format

    access_token = await platform.get_access_token(
        api_key=api_key,
        api_secret=api_secret,
    )

    if output_format == 'json':
        print(json.dumps(access_token, indent=4))
    elif output_format == 'access_token':
        print(access_token.access_token)
    else:
        for key in access_token.keys():
            print(f'{key}: {access_token[key]}')
