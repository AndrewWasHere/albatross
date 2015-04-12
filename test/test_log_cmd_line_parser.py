"""
Copyright 2015 Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
import argparse
import unittest

import log


class LogCmdLineParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        log.add_log_parser_arguments(self.parser)

    def test_arguments(self):
        args = self.parser.parse_args([])

        self.assertTrue(hasattr(args, 'log'))
        self.assertTrue(hasattr(args, 'v'))

    def test_configure_defaults(self):
        args = self.parser.parse_args([])
        settings = log.configure_logging(args)

        self.assertEqual(settings['stream_settings']['level'], log.WARNING)
        self.assertFalse('file_settings' in settings)

    def test_configure_level(self):
        def check_level():
            log_levels = (log.WARNING, log.INFO, log.DEBUG, log.NOTSET)
            settings = log.configure_logging(args)
            self.assertEqual(
                settings['stream_settings']['level'],
                log_levels[idx]
            )

        # Already tested no vees in test_configure_defaults.
        for idx in range(1, 4):
            cmdline = '-' + 'v' * idx
            args = self.parser.parse_args([cmdline])
            check_level()

            cmdline = ['-v' for _ in range(idx)]
            args = self.parser.parse_args(cmdline)
            check_level()

    def test_large_v(self):
            # Must have more than 4 vees for test to be correct.
            args = self.parser.parse_args(['-vvvvv'])
            settings = log.configure_logging(args)
            self.assertEqual(
                settings['stream_settings']['level'],
                log.NOTSET
            )

    def test_log_to_file(self):
        log_path = 'command/line/log/path'
        args = self.parser.parse_args(['--log', log_path])
        settings = log.configure_logging(args)
        self.assertEqual(settings['file_settings']['path'], log_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
