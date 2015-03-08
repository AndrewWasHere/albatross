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


def _stream_handler(level):
    fmt = logging.Formatter(
        '%(filename)s:%(lineno)d|%(levelname)8s|%(message)s'
    )
    h = logging.StreamHandler()
    h.setLevel(level)
    h.setFormatter(fmt)
    return h


def _file_handler(path):
    fmt = logging.Formatter(
        '%(asctime)s|%(filename)s:%(lineno)d|%(levelname)8s|%(message)s'
    )
    h = logging.FileHandler(path)
    h.setLevel(NOTSET)
    h.setFormatter(fmt)
    return h


def _http_handler(level, log_url, method='POST'):
    h = logging.handlers.HTTPHandler(log_url, method)
    h.setLevel(level)
    return h