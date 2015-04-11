"""
Copyright 2015 Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>. 
"""
import os


def abs_path(path, start=None):
    """The absolute path.

    Expands user constructs and converts relative paths to absolute ones.

    Args:
        path (str): The path to expand.
        start (str or None): Absolute path to start relative expansion from
            (Can be a path to file or directory). Note: relative paths can
            give unexpected results.
            None => relative to current directory of running project.

    Returns:
        path (str): Absolute path.

    Raises:
        AttributeError: path and/or start is not a string-like object.
    """
    def dir_name(p):
        return os.path.dirname(p) if os.path.isfile(p) else p

    path = os.path.expanduser(path)
    path = os.path.abspath(
        os.path.join(dir_name(start), path) if start else path
    )
    return path