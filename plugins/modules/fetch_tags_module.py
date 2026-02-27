#!/usr/bin/python3
#
# fetch_tags_module.py for jcook3701.utils
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

import urllib.parse

import requests
from ansible.module_utils.basic import AnsibleModule


# Define a TypedDict for consistent error reporting
class APIError(dict[str, str]):
    error: str


FetchResult = list[str] | str | APIError


class PlatformConfig:
    """Class to hold platform-specific API logic."""

    def __init__(self, name: str, api_template: str, auth_type: str):
        self.name = name
        self.api_template = api_template
        self.auth_type = auth_type

    def get_url(self, owner: str, repo: str) -> str:
        # For GitLab, format owner/repo as `group%2Fproject`
        if "gitlab" in self.name:
            project_path = urllib.parse.quote_plus(f"{owner}/{repo}")
            return self.api_template.format(project_path=project_path)
        return self.api_template.format(owner=owner, repo=repo)

    def get_headers(self, token: str | None) -> dict[str, str]:
        if not token:
            return {}
        if self.auth_type == "bearer":
            return {"Authorization": f"token {token}"}
        return {"Private-Token": token}


PLATFORMS = {
    "github": PlatformConfig(
        "github", "https://api.github.com/repos/{owner}/{repo}/tags", "bearer"
    ),
    "gitlab": PlatformConfig(
        "gitlab",
        "https://gitlab.com/api/v4/projects/{project_path}/repository/tags",
        "token",
    ),
    "gitlab-freedesktop": PlatformConfig(
        "gitlab-freedesktop",
        "https://gitlab.freedesktop.org/api/v4/projects/{project_path}/repository/tags",
        "token",
    ),
}


def fetch_tags(
    platform: str, owner: str, repo: str, token: str | None, latest: bool
) -> FetchResult:
    """
    Fetch tags from a given platform's API.

    Args:
        platform (str): The platform name (e.g., 'github', 'gitlab').
        owner (str): The owner or group of the repository.
        repo (str): The repository name.
        token (str): Authentication token (if required).
        latest (bool): Whether to return only the most recent tag.

    Returns:
        list or dict: List of tags, a single tag if latest=True, or an error dictionary.
    """
    config = PLATFORMS.get(platform)

    if not config:
        return APIError(error=f"Unsupported platform: {platform}")

    url = config.get_url(owner, repo)
    headers = config.get_headers(token)

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            tags = [tag["name"] for tag in data]
            if latest:
                return tags[0] if latest and tags else tags
            return tags
        else:
            return APIError(error=f"API Request failed ({response.status_code})")
    except Exception as e:
        return APIError(error=f"Failed to fetch tags: {e!s}")


def main() -> None:
    # Define Ansible module arguments
    module_args = {
        "provider": {
            "type": "str",
            "required": True,
            "choices": ["github", "gitlab", "gitlab-freedesktop"],
        },
        "owner": {"type": "str", "required": True},
        "repo": {"type": "str", "required": True},
        "token": {"type": "str", "required": False, "no_log": True},
        "latest": {"type": "bool", "required": False, "default": False},
    }

    # Initialize Ansible module
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Extract parameters
    provider = module.params["provider"]
    owner = module.params["owner"]
    repo = module.params["repo"]
    token = module.params.get("token")
    latest = module.params["latest"]

    # Fetch tags
    result = fetch_tags(provider, owner, repo, token, latest)

    # Return results
    if isinstance(result, dict) and "error" in result:
        module.fail_json(msg=result["error"])
    else:
        module.exit_json(changed=False, tags=result)


if __name__ == "__main__":
    main()
