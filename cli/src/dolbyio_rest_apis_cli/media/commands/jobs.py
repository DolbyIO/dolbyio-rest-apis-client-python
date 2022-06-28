"""
Command: Jobs
"""

from argparse import _SubParsersAction, Namespace
from dolbyio_rest_apis.media import jobs
import json

def command_name() -> str:
    return 'jobs'

def add_arguments(sub_parsers: _SubParsersAction) -> None:
    parser = sub_parsers.add_parser(command_name(), help='Jobs')

    parser.add_argument(
		'-a', '--access_token',
		help='Your API Access Token.',
		required=True,
		type=str
	)

    parser.add_argument(
		'--after',
		help='Query jobs that were submitted at or after the specified date and time (inclusive).',
		required=False,
		type=str
	)

    parser.add_argument(
		'--before',
		help='''
        Query jobs that were submitted at or before the specified date and time (inclusive).
        The `submitted_before` must be the same or later than `submitted_after`.
        ''',
		required=False,
		type=str
	)

    parser.add_argument(
		'--status',
		help='Query jobs that were submitted at or after the specified date and time (inclusive).',
		required=False,
		type=str
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
    after = args.after
    before = args.before
    status = args.status

    all_jobs = await jobs.list_all_jobs(
        access_token=access_token,
        submitted_after=after,
        submitted_before=before,
        status=status,
    )

    if args.output_format == 'json':
        print(json.dumps(all_jobs, indent=4))
    else:
        job_id = 0
        for job in all_jobs:
            job_id += 1
            print(f'Job #{job_id}/{len(all_jobs)}:')
            for key in job.keys():
                print(f' {key}: {job[key]}')
            print()
