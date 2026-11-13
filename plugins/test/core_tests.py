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

from collections.abc import Callable
from typing import Any

DOCUMENTATION = r"""
---
name: list
short_description: Verify if a variable is a native Python list
description:
    - This test checks if the provided value is a Jinja2/Python list.
    - It is used to differentiate between a single string (like a package name) and a list of strings.
version_added: "1.0.0"
author:
    - Jared Cook
notes:
    - In Jinja2, strings are considered sequences. This test specifically checks for the list type to avoid iterating over string characters.
"""

EXAMPLES = r"""
# Check if a variable is a list before looping
- name: Install packages
  ansible.builtin.apt:
    name: "{{ pkg_list if pkg_list is list else [pkg_list] }}"

# Use in a conditional
- name: Debug if it is a list
  ansible.builtin.debug:
    msg: "This is a list"
  when: my_var is list
"""


def is_list(v: Any) -> bool:
    """Check if the object is a native Python list."""
    return isinstance(v, list)


class TestModule:
    """Ansible core list test plugin."""

    def tests(self) -> dict[str, Callable[[Any], bool]]:
        """Return the dictionary of registered tests."""
        return {
            "list": is_list,
        }
