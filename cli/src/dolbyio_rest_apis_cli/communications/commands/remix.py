"""
Command: Remix
"""

from argparse import _SubParsersAction, Namespace
from dolbyio_rest_apis.communications import remix
import json

def command_name() -> str:
    return 'remix'

def add_arguments(sub_parsers: _SubParsersAction) -> None:
    parser = sub_parsers.add_parser(command_name(), help='Remix')

    parser.add_argument(
		'-a', '--access_token',
		help='Your API Access Token.',
		required=True,
		type=str
	)

    parser.add_argument(
		'--cid',
		help='Identifier of the conference.',
		required=True,
		type=str
	)

    parser.add_argument(
		'--start',
		help='Start the remix of the specified conference.',
		action='store_true',
		dest='start',
		default=False
	)

    parser.add_argument(
		'-o', '--output',
		help='Set the output format.',
		dest='output_format',
		default='json',
        choices=[ 'json', 'text' ]
	)

async def execute_command(args: Namespace) -> None:
    access_token = args.access_token
    cid = args.cid
    start = args.start
    output_format = args.output_format

    if start:
        remix_status = await remix.start(
            access_token=access_token,
            conference_id=cid
        )
    else:
        remix_status = await remix.get_status(
            access_token=access_token,
            conference_id=cid
        )

    if output_format == 'json':
        print(json.dumps(remix_status, indent=4))
    else:
        for key in remix_status.keys():
            print(f'{key}: {remix_status[key]}')
