"""
Copyright 2015 Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
from contextlib import contextmanager
import logging
import logging.handlers

# Log levels.
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

DEFAULT_TCP_LOGGING_PORT = logging.handlers.DEFAULT_TCP_LOGGING_PORT

# Remapped interfaces.
get_logger = logging.getLogger


@contextmanager
def logger(stream_settings=None, file_settings=None, http_settings=None):
    """Logging context manager.

    Convenience wrapper to set up and tear down logging.

    Use:
        with log.logger(<settings>):
            # Do something.

    Args:
        stream_settings (dict): Settings for the stream handler, if using.
        file_settings (dict): Settings for the file handler, if using.
        http_settings (dict): Settings for the http handler, if using.
    """
    def base_level():
        """Returns base logging level of all settings."""
        def level(settings):
            return (settings if settings else {}).get('level', WARNING)

        return min(
            (
                level(stream_settings),
                level(file_settings),
                level(http_settings)
            )
        )

    def configured_handlers():
        """Generator of configured log handlers."""
        if stream_settings:
            yield _stream_handler(**stream_settings)

        if file_settings:
            yield _file_handler(**file_settings)

        if http_settings:
            yield _http_handler(**http_settings)

    # Execution starts here. ###################################################

    handlers = [h for h in configured_handlers()]

    root = logging.getLogger()
    root.setLevel(base_level())
    for h in handlers:
        root.addHandler(h)

    try:
        yield

    finally:
        for h in handlers:
            h.close()


def add_log_parser_arguments(parser):
    """Add log arguments to command line parser.

    Defines the following command line arguments:
    --log: path to log file (if any)
    -v: verbosity level. More => more verbose log messages.

    Args:
        parser (argparse.ArgumentParser): parser to add arguments to.

    Returns:
        parser (argparse.ArgumentParser): parser with log arguments added.
    """
    parser.add_argument(
        '--log',
        nargs='?',
        default=None,
        help='Path to log file.'
    )
    parser.add_argument(
        '-v',
        action='count',
        default=0,
        help='Verbosity of log messages.'
    )

    return parser


def configure_logging(args):
    """Configure logging based on command line arguments.

    Args:
        args (argparse.Namespace): command line arguments containing those
            allowed by log_parser_arguments().

    Returns:
        settings (dict): Log settings consumed by logger() context manager.
    """
    log_levels = (WARNING, INFO, DEBUG, NOTSET)
    level = log_levels[min(args.v, len(log_levels) - 1)]
    settings = {
        'stream_settings': {
            'level': level
        }
    }
    if args.log:
        settings['file_settings'] = {
            'path': args.log  # Caller is responsible for expanding path.
        }

    return settings


def _stream_handler(stream=None, level=None):
    level = level or WARNING
    fmt = logging.Formatter(
        '%(filename)s:%(lineno)d|%(levelname)8s|%(message)s'
        if level <= INFO else
        '%(levelname)8s|%(message)s'
    )
    h = logging.StreamHandler(stream)
    h.setLevel(level)
    h.setFormatter(fmt)
    return h


def _file_handler(path, level=None):
    fmt = logging.Formatter(
        '%(asctime)s|%(filename)s:%(lineno)d|%(levelname)8s|%(message)s'
    )
    level = level or NOTSET
    h = logging.FileHandler(path)
    h.setLevel(level)
    h.setFormatter(fmt)
    return h


def _http_handler(level, log_url, method='POST'):
    h = logging.handlers.HTTPHandler(log_url, method)
    h.setLevel(level)
    return h