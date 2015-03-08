"""
Copyright 2015 Andrew Lin.

This file is part of Audiolens.

Audiolens is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Audiolens is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Audiolens.  If not, see <http://www.gnu.org/licenses/>.
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
    """Logging context manager."""
    def base_level():
        """Returns base logging level of all settings."""
        default_level = WARNING
        return min(
            (
                (stream_settings if stream_settings else {}).get(
                    'level', default_level
                ),
                (file_settings if file_settings else {}).get(
                    'level', default_level
                ),
                (http_settings if http_settings else {}).get(
                    'level', default_level
                )
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

    # Exectuion starts here. ###################################################

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