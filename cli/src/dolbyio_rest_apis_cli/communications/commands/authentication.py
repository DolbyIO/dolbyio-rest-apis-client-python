"""
Command: Authentication
"""

from argparse import _SubParsersAction, Namespace
from dolbyio_rest_apis.communications import authentication
import json

def command_name() -> str:
    return 'auth'

def add_arguments(sub_parsers: _SubParsersAction) -> None:
    parser = sub_parsers.add_parser(command_name(), help='Authentication')

    parser.add_argument(
		'-k', '--consumer_key',
		help='Your Dolby.io Consumer Key',
		default='',
		type=str
	)

    parser.add_argument(
		'-s', '--consumer_secret',
		help='Your Dolby.io Consumer Secret',
		default='',
		type=str
	)

    parser.add_argument(
		'-e', '--expires_in',
		help='''
        (Optional) Access token expiration time in seconds.
        The maximum value is 2,592,000, indicating 30 days. If no value is specified,
        the default is 600, indicating ten minutes.
        ''',
		default=None,
		type=int
	)

    parser.add_argument(
		'--api',
		help='Request an API Access Token otherwise a Client Access Token will be returned.',
		action='store_true',
		dest='api',
		default=False
	)

    parser.add_argument(
		'-o', '--output',
		help='Set the output format.',
		dest='output_format',
		default='json',
        choices=[ 'json', 'text', 'access_token' ]
	)

async def execute_command(args: Namespace) -> None:
    consumer_key = args.consumer_key
    consumer_secret = args.consumer_secret
    expires_in = args.expires_in
    api = args.api
    output_format = args.output_format

    if api:
        access_token = await authentication.get_api_access_token(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            expires_in=expires_in
        )
    else:
        access_token = await authentication.get_client_access_token(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            expires_in=expires_in
        )

    if output_format == 'json':
        print(json.dumps(access_token, indent=4))
    elif output_format == 'access_token':
        print(access_token.access_token)
    else:
        for key in access_token.keys():
            print(f'{key}: {access_token[key]}')
