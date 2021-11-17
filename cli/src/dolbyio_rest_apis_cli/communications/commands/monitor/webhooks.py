"""
Command: Monitor / Webhooks
"""

from argparse import _SubParsersAction, Namespace
from dolbyio_rest_apis.communications.monitor import webhooks
import json

def command_name() -> str:
    return 'webhooks'

def add_arguments(sub_parsers: _SubParsersAction) -> None:
    parser = sub_parsers.add_parser(command_name(), help='Webhooks')

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
		'--from',
		help='The beginning of the time range (in milliseconds that have elapsed since epoch).',
		required=False,
		dest='tr_from',
		type=int,
        default=0
	)

    parser.add_argument(
		'--to',
		help='The end of the time range (in milliseconds that have elapsed since epoch).',
		required=False,
		dest='tr_to',
		type=int,
        default=9999999999999
	)

    parser.add_argument(
		'--filter',
		help='''
            The Webhook event type or an expression of its type (for example `Recording.Live.InProgress` or `Rec.*`).
            The default value of the type parameter returns all types of Webhooks.
            ''',
		required=False,
		type=str,
        default=None
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
    tr_from = args.tr_from
    tr_to = args.tr_to
    filter_type = args.filter
    output_format = args.output_format

    events = await webhooks.get_all_events(
        access_token=access_token,
        conference_id=cid,
        tr_from=tr_from,
        tr_to=tr_to,
        filter_type=filter_type
    )

    if output_format == 'json':
        print(json.dumps(events, indent=4))
    else:
        ev_id = 0
        for event in events:
            ev_id += 1
            print(f'Webhook event #{ev_id}/{len(events)}:')
            for key in event.keys():
                print(f' {key}: {event[key]}')
            print()
