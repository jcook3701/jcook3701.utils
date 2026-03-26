#!/usr/bin/python3
#
# core_tests.py for jcook3701.utils
#
# SPDX-FileCopyrightText: Jared Cook
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest

from ansible_collections.jcook3701.utils.plugins.test.core_tests import (
    TestModule,
    is_list,
)


TestModule.__test__ = False


class TestCoreTests(unittest.TestCase):
    """Test cases for the core_tests plugin."""

    def setUp(self) -> None:
        """Initialize the plugin and extracted tests."""
        self.plugin = TestModule()
        self.registered_tests = self.plugin.tests()

    def test_registration(self) -> None:
        """Verify 'list' is correctly registered in the plugin."""
        self.assertIn("list", self.registered_tests)
        self.assertEqual(self.registered_tests["list"], is_list)

    def test_is_list_valid(self) -> None:
        """Verify is_list returns True for actual list objects."""
        self.assertTrue(is_list([]))
        self.assertTrue(is_list([1, 2, 3]))
        self.assertTrue(is_list(["a", "b", "c"]))

    def test_is_list_invalid(self) -> None:
        """Verify is_list returns False for non-list types."""
        self.assertFalse(is_list("not a list"))
        self.assertFalse(is_list(123))
        self.assertFalse(is_list({"key": "value"}))
        self.assertFalse(is_list((1, 2)))  # Tuples are not lists
        self.assertFalse(is_list(None))


if __name__ == "__main__":
    unittest.main()
