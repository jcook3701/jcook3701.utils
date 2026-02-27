#!/usr/bin/python3
#
# ansible_doc_gen.py for jcook3701.utils
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

import glob
from pathlib import Path
from typing import Any

import yaml
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: ansible_doc_gen
short_description: Generate markdown documentation from Ansible roles and playbooks
description:
    - This module scans a roles directory and optional playbooks directory to generate markdown documentation files.
    - It extracts defaults, tasks, and metadata from roles and formats them into Markdown.
version_added: "1.0.0"
author:
    - jcook3701
options:
    roles_path:
        description: The path to the directory containing Ansible roles.
        type: str
        required: true
    playbooks_path:
        description: The path to the directory containing Ansible playbooks.
        type: str
        required: false
    output_path:
        description: The directory where generated markdown files will be saved.
        type: str
        required: true
    include_tasks:
        description: Whether to include role tasks in the documentation.
        type: bool
        default: true
    include_defaults:
        description: Whether to include role defaults in the documentation.
        type: bool
        default: true
    include_meta:
        description: Whether to include role metadata in the documentation.
        type: bool
        default: true
"""

EXAMPLES = r"""
- name: Generate documentation for local roles
  jcook3701.utils.ansible_doc_gen:
    roles_path: "./roles"
    output_path: "./docs/roles"
    include_meta: true

- name: Generate docs for roles and playbooks
  jcook3701.utils.ansible_doc_gen:
    roles_path: "./roles"
    playbooks_path: "./playbooks"
    output_path: "./dist/docs"
"""

RETURN = r"""
generated_files:
    description: A list of paths to the markdown files that were created.
    returned: always
    type: list
    sample: ["/tmp/docs/my_role.md", "/tmp/docs/site_playbook.md"]
message:
    description: A summary message of the operation.
    returned: always
    type: str
    sample: "Docs generated at /tmp/docs"
"""


def yaml_to_md(data: Any) -> str:
    """Converts YAML data to a string without sorting keys."""
    return yaml.dump(data, sort_keys=False)


def run_module() -> None:
    """Main logic for the Ansible module."""
    module_args = {
        "roles_path": {"type": "str", "required": True},
        "playbooks_path": {"type": "str", "required": False, "default": None},
        "output_path": {"type": "str", "required": True},
        "include_tasks": {"type": "bool", "default": True},
        "include_defaults": {"type": "bool", "default": True},
        "include_meta": {"type": "bool", "default": True},
    }

    result: dict[str, Any] = {"changed": False, "message": "", "generated_files": []}

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    roles_path = module.params["roles_path"]
    playbooks_path = module.params["playbooks_path"]
    output_path = Path(module.params["output_path"])
    include_tasks = module.params["include_tasks"]
    include_defaults = module.params["include_defaults"]
    include_meta = module.params["include_meta"]

    output_path.mkdir(parents=True, exist_ok=True)

    # Process roles
    for role_dir in Path(roles_path).iterdir():
        if not role_dir.is_dir():
            continue
        role_name = role_dir.name
        md = f"# Role: {role_name}\n\n"

        if include_defaults:
            defaults_file = role_dir / "defaults/main.yml"
            if defaults_file.exists():
                defaults = yaml.safe_load(defaults_file.read_text())
                md += f"## Defaults\n```yaml\n{yaml_to_md(defaults)}```\n\n"

        if include_tasks:
            tasks_files = glob.glob(str(role_dir / "tasks/*.yml"))
            if tasks_files:
                md += "## Tasks\n"
                for tf in tasks_files:
                    tasks = yaml.safe_load(Path(tf).read_text())
                    md += f"### {Path(tf).name}\n```yaml\n{yaml_to_md(tasks)}```\n\n"

        if include_meta:
            meta_file = role_dir / "meta/main.yml"
            if meta_file.exists():
                meta = yaml.safe_load(meta_file.read_text())
                md += f"## Meta\n```yaml\n{yaml_to_md(meta)}```\n\n"

        output_file = output_path / f"{role_name}.md"
        output_file.write_text(md)
        result["generated_files"].append(str(output_file))

    # Optional: process playbooks
    if playbooks_path:
        for pb_file in glob.glob(f"{playbooks_path}/*.yml"):
            pb_name = Path(pb_file).stem
            tasks = yaml.safe_load(Path(pb_file).read_text())
            md = f"# Playbook: {pb_name}\n\n```yaml\n{yaml_to_md(tasks)}```\n"
            output_file = output_path / f"{pb_name}.md"
            output_file.write_text(md)
            result["generated_files"].append(str(output_file))

    result["changed"] = True
    result["message"] = f"Docs generated at {output_path}"
    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()
