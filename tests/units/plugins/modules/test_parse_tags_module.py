#!/usr/bin/python3
#
# test_parse_tags_module.py for jcook3701.utils
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

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

# FQCN Import for the jcook3701.utils collection
from ansible_collections.jcook3701.utils.plugins.modules.parse_tags_module import (
    main,
    parse_tag,
    parse_tags,
)


@pytest.mark.parametrize(
    "tag,expected",
    [
        ("v1.2.3", {"major": 1, "minor": 2, "patch": 3, "project": None}),
        ("emacs-29.4", {"major": 29, "minor": 4, "patch": 0, "project": "emacs"}),
        ("2.0", {"major": 2, "minor": 0, "patch": 0, "project": None}),
        (
            "ansible-core-2.14.2",
            {"major": 2, "minor": 14, "patch": 2, "project": "ansible-core"},
        ),
    ],
)
def test_parse_tag_formats(tag: str, expected: dict[str, Any]) -> None:
    """Verify regex patterns for various version string formats."""
    result = parse_tag(tag)
    assert result["major"] == expected["major"]
    assert result["minor"] == expected["minor"]
    assert result["patch"] == expected["patch"]
    assert result["project"] == expected["project"]
    assert result["raw_tag"] == tag


def test_parse_tag_unrecognized() -> None:
    """Verify error handling for invalid tag formats."""
    tag = "invalid_version_123"
    result = parse_tag(tag)
    assert "error" in result
    assert result["error"] == "Unrecognized format"
    assert result["raw_tag"] == tag


def test_parse_tags_list() -> None:
    """Verify bulk parsing of a list of tags."""
    tags = ["v1.0.0", "2.0"]
    results = parse_tags(tags)
    assert len(results) == 2
    assert results[0]["major"] == 1
    assert results[1]["major"] == 2


@patch(
    "ansible_collections.jcook3701.utils.plugins.modules.parse_tags_module.AnsibleModule"
)
def test_main_success(mock_ansible_module: MagicMock) -> None:
    """Test successful module execution via main()."""
    mock_module_instance = MagicMock()
    mock_module_instance.params = {"tags": ["v1.2.3", "project-9.0"]}
    mock_ansible_module.return_value = mock_module_instance

    main()

    # Capture the output sent to exit_json
    mock_module_instance.exit_json.assert_called_once()
    args, kwargs = mock_module_instance.exit_json.call_args

    assert kwargs["changed"] is False
    assert len(kwargs["parsed_tags"]) == 2
    assert kwargs["parsed_tags"][0]["raw_tag"] == "v1.2.3"


@patch(
    "ansible_collections.jcook3701.utils.plugins.modules.parse_tags_module.AnsibleModule"
)
def test_main_error_handling(mock_ansible_module: MagicMock) -> None:
    """Test module behavior when an unexpected exception occurs."""
    mock_module_instance = MagicMock()
    # Passing None to trigger a TypeError in parse_tags
    mock_module_instance.params = {"tags": None}
    mock_ansible_module.return_value = mock_module_instance

    main()

    mock_module_instance.fail_json.assert_called_once()
    assert "Error parsing tags" in mock_module_instance.fail_json.call_args[1]["msg"]
