"""
Copyright 2015 Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
import io
import unittest

import log


class StreamHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()
        self.settings = {
            'stream': self.stream
        }
        self.logger = log.get_logger(__name__)
        self.critical_msg = 'critical log message'
        self.error_msg = 'error log message'
        self.warning_msg = 'warning log message'
        self.info_msg = 'info log message'
        self.debug_msg = 'debug log message'

    def test_critical(self):
        # Setup.
        self.settings['level'] = log.CRITICAL

        # Run.
        with log.logger(stream_settings=self.settings):
            self._write_log_messages()

        output = self.stream.getvalue()

        # Test.
        self.assertTrue(self.critical_msg in output)
        self.assertFalse(self.error_msg in output)
        self.assertFalse(self.warning_msg in output)
        self.assertFalse(self.info_msg in output)
        self.assertFalse(self.debug_msg in output)

    def test_error(self):
        # Setup.
        self.settings['level'] = log.ERROR

        # Run.
        with log.logger(stream_settings=self.settings):
            self._write_log_messages()

        output = self.stream.getvalue()

        # Test.
        self.assertTrue(self.critical_msg in output)
        self.assertTrue(self.error_msg in output)
        self.assertFalse(self.warning_msg in output)
        self.assertFalse(self.info_msg in output)
        self.assertFalse(self.debug_msg in output)

    def test_warning(self):
        # Setup.
        self.settings['level'] = log.WARNING

        # Run.
        with log.logger(stream_settings=self.settings):
            self._write_log_messages()

        output = self.stream.getvalue()

        # Test.
        self.assertTrue(self.critical_msg in output)
        self.assertTrue(self.error_msg in output)
        self.assertTrue(self.warning_msg in output)
        self.assertFalse(self.info_msg in output)
        self.assertFalse(self.debug_msg in output)

    def test_info(self):
        # Setup.
        self.settings['level'] = log.INFO

        # Run.
        with log.logger(stream_settings=self.settings):
            self._write_log_messages()

        output = self.stream.getvalue()

        # Test.
        self.assertTrue(self.critical_msg in output)
        self.assertTrue(self.error_msg in output)
        self.assertTrue(self.warning_msg in output)
        self.assertTrue(self.info_msg in output)
        self.assertFalse(self.debug_msg in output)

    def test_debug(self):
        # Setup.
        self.settings['level'] = log.DEBUG

        # Run.
        with log.logger(stream_settings=self.settings):
            self._write_log_messages()

        output = self.stream.getvalue()

        # Test.
        self.assertTrue(self.critical_msg in output)
        self.assertTrue(self.error_msg in output)
        self.assertTrue(self.warning_msg in output)
        self.assertTrue(self.info_msg in output)
        self.assertTrue(self.debug_msg in output)

    def _write_log_messages(self):
        self.logger.critical(self.critical_msg)
        self.logger.error(self.error_msg)
        self.logger.warning(self.warning_msg)
        self.logger.info(self.info_msg)
        self.logger.debug(self.debug_msg)


if __name__ == '__main__':
    unittest.main(verbosity=2)
