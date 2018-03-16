from cakebot import __version__
from cakebot.bot import Bot


def main():
    import argparse

    parser = argparse.ArgumentParser(description='AIRC CakeBot')
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__),
    )
    parser.add_argument(
        '--config_path',
        '-c',
        default='config.py',
        type=str,
        help='Path to AIRC bot config json file',
    )
    args = parser.parse_args()

    Bot.from_config_path(args.config_path).start()


if __name__ == '__main__':
    import sys
    sys.exit(main())
