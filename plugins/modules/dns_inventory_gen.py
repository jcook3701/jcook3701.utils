#!/usr/bin/python3
#
# test_dns_inventory_gen.py for jcook3701.utils
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


from __future__ import annotations  # Allows forward references and cleaner typing

import re
from ipaddress import ip_address
from typing import Any

import yaml
from ansible.module_utils.basic import AnsibleModule

# Type Aliases using native generics
DnsRecord = list[str]


def parse_dns_zone(zone_file: str) -> list[DnsRecord]:
    """Parse the DNS zone file using native list generics."""
    records: list[DnsRecord] = []
    with open(zone_file) as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith(";"):
                continue
            parts = re.split(r"\s+", line)
            if len(parts) >= 4 and parts[2] in ["A", "AAAA"]:
                if "@" not in parts[0]:
                    records.append(parts)
    return records


def run_module() -> None:
    module_args = {
        "zone_file": {"type": "str", "required": True},
        "output_file": {"type": "str", "required": True},
    }

    result: dict[str, Any] = {"changed": False, "message": ""}

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    zone_path: str = module.params["zone_file"]
    dest_path: str = module.params["output_file"]

    try:
        records = parse_dns_zone(zone_path)

        # Maps IP -> Hostname (native dict)
        ip_to_hostname: dict[str, str] = {}
        for record in records:
            hostname, _, _, ip = record[:4]
            ip_to_hostname[ip] = hostname

        sorted_ips = sorted(ip_to_hostname.keys(), key=ip_address)

        inventory = {
            "all": {
                "hosts": {ip_to_hostname[ip]: {"ansible_host": ip} for ip in sorted_ips}
            }
        }

        # Check for changes if using check_mode
        # In a real module, you'd compare existing file content here
        with open(dest_path, "w") as f:
            yaml.dump(inventory, f, default_flow_style=False)

        result["changed"] = True
        result["message"] = f"Inventory generated at {dest_path}"
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Failed to process zone file: {e!s}", **result)


if __name__ == "__main__":
    run_module()
