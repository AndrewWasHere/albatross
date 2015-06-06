"""
Copyright 2015 Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
import os
import unittest
import sys

import path


class AbspathTestCase(unittest.TestCase):
    def test_absolute(self):
        p = os.path.join(os.sep, 'absolute', 'path')
        p_prime = path.abs_path(p)
        self.assertEqual(p_prime, p)

    def test_relative(self):
        p = os.path.join('relative', 'to', 'curdir')
        p_gold = os.path.join(os.path.abspath(os.path.curdir), p)
        p_prime = path.abs_path(p)
        self.assertEqual(p_prime, p_gold)

    def test_absolute_to(self):
        root = os.path.dirname(__file__)
        p = os.path.join(os.sep, 'absolute', 'path')

        # File as start.
        p_prime = path.abs_path(p, root=__file__)
        self.assertEqual(p_prime, p)

        # Directory as start.
        p_prime = path.abs_path(p, root=root)
        self.assertEqual(p_prime, p)

    def test_relative_to(self):
        root = os.path.dirname(__file__)
        p = os.path.join('relative', 'to', 'root')
        p_gold = os.path.join(root, p)

        # File as start.
        p_prime = path.abs_path(p, root=__file__)
        self.assertEqual(p_prime, p_gold)

        # Directory as start.
        p_prime = path.abs_path(p, root=root)
        self.assertEqual(p_prime, p_gold)

    def test_bad_paths(self):
        # Unallowed path types.
        with self.assertRaises(AttributeError):
            path.abs_path(1)

        with self.assertRaises(AttributeError):
            path.abs_path(None)

        # Unallowed start types.
        # Python 3.2 raises a TypeError.
        # Python 3.4 raises an AttributeError.
        # Other version are untested.
        expected_error = (
            TypeError
            if sys.version_info.major == 3 and sys.version_info.minor == 2 else
            AttributeError
        )
        with self.assertRaises(expected_error):
            path.abs_path('foo', 2)

    def test_up_dir(self):
        root = os.path.join(os.sep, 'root', 'branch')
        relative_path = os.path.join('..', 'leaf')
        p = path.abs_path(relative_path, root=root)

        self.assertEqual(p, os.path.join(os.sep, 'root', 'leaf'))

        root = __file__
        root_dir = os.path.dirname(root)
        p = os.path.abspath(os.path.join(root_dir, relative_path))
        p_prime = path.abs_path(relative_path, root)
        self.assertEqual(p_prime, p)


if __name__ == '__main__':
    unittest.main(verbosity=2)
