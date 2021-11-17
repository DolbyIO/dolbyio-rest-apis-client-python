"""
dolbyio_rest_apis_cli.communications.cli
~~~~~~~~~~~~~~~

This module contains the main entry point for the CLI.

"""

import argparse
import asyncio
from dolbyio_rest_apis_cli.core import version
from dolbyio_rest_apis_cli.communications.commands import authentication, streaming, remix
from dolbyio_rest_apis_cli.communications.commands.monitor import webhooks

async def main():
    parser = argparse.ArgumentParser(description='Dolby.io REST APIs CLI - Communications')
    sub_parsers = parser.add_subparsers(dest='command')

    version.add_arguments(parser)
    authentication.add_arguments(sub_parsers)
    remix.add_arguments(sub_parsers)
    streaming.add_arguments(sub_parsers)

    command_name_monitor = 'monitor'
    parser_monitor = sub_parsers.add_parser(command_name_monitor, help='Monitor')
    sub_parsers_monitor = parser_monitor.add_subparsers(dest='sub_command')
    webhooks.add_arguments(sub_parsers_monitor)

    args = parser.parse_args()

    if args.version:
        version.execute_command()
    elif args.command is None:
        parser.print_help()
    elif args.command == authentication.command_name():
        await authentication.execute_command(args)
    elif args.command == remix.command_name():
        await remix.execute_command(args)
    elif args.command == streaming.command_name():
        await streaming.execute_command(args)
    elif args.command == command_name_monitor:
        if args.sub_command == webhooks.command_name():
            await webhooks.execute_command(args)

def cli():
    asyncio.get_event_loop().run_until_complete(main())

if __name__ == '__main__':
    cli()
