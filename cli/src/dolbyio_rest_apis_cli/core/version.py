"""
Command: Version
"""

import argparse
import importlib

def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
		'-v', '--version',
		help='Get the version of the package',
		action='store_true',
		dest='version',
		default=False
	)

def execute_command() -> None:
    package_name = 'dolbyio_rest_apis_cli'
    package_version = importlib.metadata.version(package_name)

    print(f'Dolby.io REST APIs CLI version: {package_version}')
