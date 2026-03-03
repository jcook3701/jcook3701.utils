#!/usr/bin/python3
#
# test_fetch_tags_module.py for jcook3701.utils
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
from unittest.mock import patch, MagicMock
import pytest

# Fixed: Importing 'main' because that is what is in your source file
from ansible_collections.jcook3701.utils.plugins.modules.fetch_tags_module import (
    fetch_tags,
    main,
)

# Mock API Data
MOCK_GITHUB_TAGS: list[dict[str, str]] = [
    {"name": "v1.2.0"},
    {"name": "v1.1.0"},
    {"name": "v1.0.0"},
]


def test_fetch_tags_github_success() -> None:
    """Test successful tag retrieval from GitHub."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_GITHUB_TAGS
        mock_get.return_value = mock_response

        result = fetch_tags("github", "ansible", "ansible", None, False)

        # Verify logic
        assert isinstance(result, list)
        assert result[0] == "v1.2.0"
        assert len(result) == 3


def test_fetch_tags_latest_only() -> None:
    """Test that 'latest=True' returns a single string."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_GITHUB_TAGS
        mock_get.return_value = mock_response

        result = fetch_tags("github", "ansible", "ansible", None, True)

        assert isinstance(result, str)
        assert result == "v1.2.0"


@patch(
    "ansible_collections.jcook3701.utils.plugins.modules.fetch_tags_module.AnsibleModule"
)
@patch(
    "ansible_collections.jcook3701.utils.plugins.modules.fetch_tags_module.fetch_tags"
)
def test_main_failure(mock_fetch: MagicMock, mock_ansible_module: MagicMock) -> None:
    """Test module behavior when fetch_tags returns an error."""
    mock_module_instance = MagicMock()
    mock_module_instance.params = {
        "provider": "github",
        "owner": "ansible",
        "repo": "ansible",
        "token": None,
        "latest": False,
    }
    mock_ansible_module.return_value = mock_module_instance

    # Simulate the APIError return structure from your source
    mock_fetch.return_value = {"error": "API Request failed (404)"}

    # Calling main() as defined in your source
    main()

    mock_module_instance.fail_json.assert_called_once_with(
        msg="API Request failed (404)"
    )


@pytest.mark.parametrize(
    "platform,owner,repo,expected_url",
    [
        ("github", "jcook", "utils", "https://api.github.com/repos/jcook/utils/tags"),
        (
            "gitlab",
            "jcook",
            "utils",
            "https://gitlab.com/api/v4/projects/jcook%2Futils/repository/tags",
        ),
        (
            "gitlab-freedesktop",
            "jcook",
            "utils",
            "https://gitlab.freedesktop.org/api/v4/projects/jcook%2Futils/repository/tags",
        ),
    ],
)
def test_platform_url_generation(
    platform: str, owner: str, repo: str, expected_url: str
) -> None:
    """Verify URL generation and GitLab path encoding."""
    from ansible_collections.jcook3701.utils.plugins.modules.fetch_tags_module import (
        PLATFORMS,
    )

    config = PLATFORMS[platform]
    generated_url: str = config.get_url(owner, repo)
    assert generated_url == expected_url
