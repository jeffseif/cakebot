from cakebot import __version__
from cakebot.bot import Bot
from cakebot.logging import set_verbosity


def main():
    import argparse

    parser = argparse.ArgumentParser(description='AIRC CakeBot')
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__),
    )
    parser.add_argument(
        '-c',
        '--config_path',
        default='config.py',
        type=str,
        help='Path to AIRC bot config json file',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Increase output verbosity',
    )
    args = parser.parse_args()

    set_verbosity(args.verbose)

    Bot.from_config_path(args.config_path).start()


if __name__ == '__main__':
    import sys
    sys.exit(main())
