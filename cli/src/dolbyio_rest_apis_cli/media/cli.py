"""
dolbyio_rest_apis_cli.media.cli
~~~~~~~~~~~~~~~

This module contains the main entry point for the CLI.

"""

import argparse
import asyncio
from dolbyio_rest_apis_cli.core import version
from dolbyio_rest_apis_cli.media.commands import authentication, enhance, io, jobs, mastering, transcode

async def main():
    parser = argparse.ArgumentParser(description='Dolby.io REST APIs CLI - Media')
    sub_parsers = parser.add_subparsers(dest='command')

    version.add_arguments(parser)
    authentication.add_arguments(sub_parsers)
    enhance.add_arguments(sub_parsers)
    io.add_arguments(sub_parsers)
    jobs.add_arguments(sub_parsers)
    mastering.add_arguments(sub_parsers)
    transcode.add_arguments(sub_parsers)

    args = parser.parse_args()

    if args.version:
        version.execute_command()
    elif args.command is None:
        parser.print_help()
    elif args.command == authentication.command_name():
        await authentication.execute_command(args)
    elif args.command == enhance.command_name():
        await enhance.execute_command(args)
    elif args.command == io.command_name():
        await io.execute_command(args)
    elif args.command == jobs.command_name():
        await jobs.execute_command(args)
    elif args.command == mastering.command_name():
        await mastering.execute_command(args)
    elif args.command == transcode.command_name():
        await transcode.execute_command(args)

def cli():
    asyncio.get_event_loop().run_until_complete(main())

if __name__ == '__main__':
    cli()
