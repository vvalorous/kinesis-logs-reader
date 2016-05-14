from argparse import ArgumentParser
from datetime import datetime
import sys

from .kinesis_logs_reader import KinesisLogsReader


def print_stream(stream_name, start_time):
    reader = KinesisLogsReader(stream_name, start_time=start_time)
    for i, fields in enumerate(reader):
        if i == 0:
            keys = list(fields.keys())
            print(*keys, sep='\t')
        print(*[fields[k] for k in keys], sep='\t')


def main(argv=None):
    argv = argv or sys.argv[1:]

    argument_parser = ArgumentParser('Read logs from AWS Kinesis')
    argument_parser.add_argument(
        'stream_name', type=str, help='Name of the Kinesis stream to read'
    )
    argument_parser.add_argument(
        '--start-time',
        type=str,
        help='Time from which to start reading (default: beginning of stream)'
    )
    argument_parser.add_argument(
        '--time-format',
        type=str,
        default='%Y-%m-%d %H:%M:%S',
        help='Format string for the --start-time argument',
    )
    args = argument_parser.parse_args(argv)

    if args.start_time:
        start_time = datetime.strptime(args.start_time, args.time_format)
    else:
        start_time = None

    print_stream(args.stream_name, start_time)


if __name__ == '__main__':
    main()