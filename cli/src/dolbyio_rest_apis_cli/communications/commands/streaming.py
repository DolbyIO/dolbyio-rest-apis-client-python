"""
Command: Streaming
"""

from argparse import _SubParsersAction, Namespace
from dolbyio_rest_apis.communications import streaming
import sys

def command_name() -> str:
    return 'streaming'

def add_arguments(sub_parsers: _SubParsersAction) -> None:
    parser = sub_parsers.add_parser(command_name(), help='Streaming')

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
		'--action',
		help='Start or stop the streaming.',
		required=True,
        choices=[ 'start', 'stop' ],
		type=str
	)

    parser.add_argument(
		'--target',
		help='Perform the operation for RTMP.',
		required=True,
        choices=[ 'rtmp' ],
		type=str
	)

    parser.add_argument(
		'-u', '--url',
		help='The destination URI provided by the RTMP service.',
		nargs='*',
        required='start' in sys.argv and 'rtmp' in sys.argv,
		type=str
	)

async def execute_command(args: Namespace) -> None:
    access_token = args.access_token
    cid = args.cid
    action = args.action
    target = args.target
    url = args.url

    if target == 'rtmp':
        if action == 'start':
            print(f'Start the streaming to RTMP for the conference "{cid}".')
            print(f' - {url}')

            await streaming.start_rtmp(
                access_token=access_token,
                conference_id=cid,
                rtmp_url=url
            )
        elif action == 'stop':
            print(f'Stop the streaming to RTMP for the conference "{cid}".')

            await streaming.stop_rtmp(
                access_token=access_token,
                conference_id=cid
            )
