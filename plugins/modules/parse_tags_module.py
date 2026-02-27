#!/usr/bin/python3
#
# parse_tags_module.py for jcook3701.utils
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

import re
from typing import TypedDict

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: parse_tags_module
short_description: Parse version tags into structured components
description:
    - This module takes a list of version strings (tags) and parses them into major, minor, and patch components.
    - Supports formats like v1.2.3, project-1.2.3, or raw 1.2.3.
version_added: "1.0.0"
author:
    - jcook3701
options:
    tags:
        description: A list of tag strings to be parsed.
        type: list
        elements: str
        required: true
"""

EXAMPLES = r"""
- name: Parse a list of version tags
  jcook3701.utils.parse_tags_module:
    tags:
      - v1.2.3
      - emacs-29.4
      - 2.0
"""

RETURN = r"""
parsed_tags:
    description: A list of dictionaries containing parsed version components.
    returned: always
    type: list
    elements: dict
    contains:
        raw_tag:
            description: The original tag string.
            type: str
        project:
            description: The project name if extracted from the tag.
            type: str
        major:
            description: The major version number.
            type: int
        minor:
            description: The minor version number.
            type: int
        patch:
            description: The patch version number.
            type: int
        error:
            description: Error message if the format was unrecognized.
            type: str
"""


class ParsedTag(TypedDict, total=False):
    raw_tag: str
    project: str | None
    major: int
    minor: int
    patch: int
    error: str  # Only present if parsing fails


def parse_tag(tag: str) -> ParsedTag:
    """
    Parse a single tag to extract version components.
    Supports flexible tag formats such as:
    - v<major>.<minor>.<patch> (e.g., v1.2.3)
    - <project>-<major>.<minor>.<patch> (e.g., emacs-29.4)
    - <major>.<minor>.<patch> (e.g., 1.2.3)
    """
    patterns = [
        r"^(?P<project>[a-zA-Z0-9_-]+)-(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$",
        r"^v(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$",
        r"^(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$",
    ]

    for pattern in patterns:
        match = re.match(pattern, tag.strip("[]"))
        if match:
            return ParsedTag(
                raw_tag=tag,
                project=(
                    match.group("project") if "project" in match.groupdict() else None
                ),
                major=int(match.group("major")),
                minor=int(match.group("minor")),
                patch=int(match.group("patch")) if match.group("patch") else 0,
            )

    return ParsedTag(raw_tag=tag, error="Unrecognized format")


def parse_tags(tags: str) -> list[ParsedTag]:
    """
    Parse a list of tags and return detailed information for each tag.
    """
    return [parse_tag(tag) for tag in tags]


def main() -> None:
    module_args = {
        "tags": {
            "type": "list",
            "required": True,
            "elements": "str",
        },  # Accepts a list of tag strings
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Get the input list of tags
    tags = module.params["tags"]

    try:
        parsed_tags = parse_tags(tags)
        module.exit_json(changed=False, parsed_tags=parsed_tags)
    except Exception as e:
        module.fail_json(msg=f"Error parsing tags: {e!s}")


if __name__ == "__main__":
    main()
