#!/usr/bin/env python3

import argparse
import sys
import logging

from app import conf, deps, command


def run(argv: list, cfg: conf.Config) -> None:
    args = _parse_args(argv)
    dep = deps.Dependencies(cfg)
    if args.cmd == command.ConfigDebugCommand.NAME:
        command.ConfigDebugCommand(
            file_path=args.file_path,
            parser=dep.parser).run()
    elif args.cmd == command.KafkaApplyCommand.NAME:
        command.KafkaApplyCommand(
            parser=dep.parser,
            resolver=dep.resolver,
            transitioner=dep.transitioner,
            file_path=args.file_path).run()
    elif args.cmd == command.KafkaDumpCommand.NAME:
        command.KafkaDumpCommand(
            parser=dep.parser,
            resolver=dep.resolver,
            dest_path=args.dest_path).run()
    elif args.cmd == command.KafkaPlanCommand.NAME:
        command.KafkaPlanCommand(
            parser=dep.parser,
            resolver=dep.resolver,
            file_path=args.file_path).run()
    else:
        raise ValueError(f"Unmapped command [{args.cmd}]")


def _parse_args(argv: list) -> any:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    cfg_debug = subparsers.add_parser(
        command.ConfigDebugCommand.NAME,
        help=command.ConfigDebugCommand.HELP)
    cfg_debug.add_argument('file_path')

    sys_apply = subparsers.add_parser(
        command.KafkaApplyCommand.NAME,
        help=command.KafkaApplyCommand.HELP)
    sys_apply.add_argument('file_path')

    subparsers.add_parser(
        command.KafkaDescribeCommand.NAME,
        help=command.KafkaDescribeCommand.HELP)

    sys_dump = subparsers.add_parser(
        command.KafkaDumpCommand.NAME,
        help=command.KafkaDumpCommand.HELP)
    sys_dump.add_argument('dest_path')

    sys_plan = subparsers.add_parser(
        command.KafkaPlanCommand.NAME,
        help=command.KafkaPlanCommand.HELP)
    sys_plan.add_argument('file_path')

    return parser.parse_args(argv)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        config = conf.from_environment()
        run(sys.argv[1:], config)
        print("\nOperation completed")
    except Exception as err:
        print(f"\nCommand failed:\n{str(err)}")
        exit(1)
