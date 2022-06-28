"""
Command: Enhance
"""

from argparse import _SubParsersAction, Namespace
from dolbyio_rest_apis.media import enhance
import json

def command_name() -> str:
    return 'enhance'

def add_arguments(sub_parsers: _SubParsersAction) -> None:
    parser = sub_parsers.add_parser(command_name(), help='Enhance API')

    parser.add_argument(
		'-a', '--access_token',
		help='Your API Access Token.',
		required=True,
		type=str
	)

    sub_parsers_io = parser.add_subparsers(dest='sub_command')

    start_parser = sub_parsers_io.add_parser('start', help='Starts enhancing to improve your media.')

    start_parser.add_argument(
		'--file',
		help='''
        File that contains the job description as a JSON payload.
        You can find the definition at this URL: https://docs.dolby.io/media-apis/reference/media-enhance-post
        ''',
		required=True,
		type=str
	)

    result_parser = sub_parsers_io.add_parser('result', help='Gets Enhance Results')

    result_parser.add_argument(
		'-i', '--job_id',
		help='Job identifier.',
		required=True,
		type=str
	)

    result_parser.add_argument(
		'-o', '--output',
		help='Set the output format.',
		dest='output_format',
		default='json',
        choices=[ 'json', 'text' ]
	)

async def execute_command(args: Namespace) -> None:
    access_token = args.access_token

    if args.sub_command == 'start':
        file_path = args.file
        with open(file_path, 'r', encoding='UTF-8') as f:
            job_content = f.read()

        job_id = await enhance.start(
            access_token=access_token,
            job_content=job_content
        )

        print(job_id)
    elif args.sub_command == 'result':
        job_id = args.job_id
        job_result = await enhance.get_results(
            access_token=access_token,
            job_id=job_id
        )

        if args.output_format == 'json':
            print(json.dumps(job_result, indent=4))
        else:
            for key in job_result.keys():
                print(f'{key}: {job_result[key]}')
