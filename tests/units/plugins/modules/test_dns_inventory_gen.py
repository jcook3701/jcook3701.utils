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


from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, NonCallableMagicMock, mock_open, patch

import yaml
from ansible_collections.jcook3701.utils.plugins.modules.dns_inventory_gen import (
    parse_dns_zone,
    run_module,
)

# Mock DNS Zone file content
MOCK_ZONE_DATA: str = """
; Comment line
@       IN      SOA     ns1.example.com. admin.example.com. ( 2026030301 3600 600 1209600 3600 )
ns1     IN      A       192.168.1.10
web01   IN      A       192.168.1.2
db01    IN      AAAA    2001:db8::1
web02   IN      A       192.168.1.5
"""


def test_parse_dns_zone() -> None:
    """Verify that only A/AAAA records are extracted and @ is ignored."""
    # mypy requires explicit type for mock_open to handle context manager typing
    m = mock_open(read_data=MOCK_ZONE_DATA)
    with patch("builtins.open", m):
        records = parse_dns_zone("dummy_path")

    assert len(records) == 4
    assert any("web01" in r for r in records)
    assert not any("@" in r for r in records)


@patch(
    "ansible_collections.jcook3701.utils.plugins.modules.dns_inventory_gen.AnsibleModule"
)
@patch(
    "ansible_collections.jcook3701.utils.plugins.modules.dns_inventory_gen.parse_dns_zone"
)
@patch("builtins.open", new_callable=mock_open)
def test_run_module_success(
    mock_file: MagicMock, mock_parse: MagicMock, mock_ansible_module: MagicMock
) -> None:
    """Test the full module execution and inventory sorting."""
    # Setup Mock Inputs
    mock_module_instance = MagicMock()
    mock_module_instance.params = {
        "zone_file": "db.example.com",
        "output_file": "inventory.yml",
    }
    mock_module_instance.check_mode = False
    mock_ansible_module.return_value = mock_module_instance

    # Setup Mock Parse Results (Unsorted)
    mock_parse.return_value = [
        ["web02", "IN", "A", "192.168.1.5"],
        ["web01", "IN", "A", "192.168.1.2"],
    ]

    # Execute Module
    run_module()

    # Verify Output Data
    # cast write calls to string for analysis
    handle = mock_file()
    written_content: str = "".join(
        str(call.args[0]) for call in handle.write.call_args_list
    )
    output_inventory: dict[str, Any] = yaml.safe_load(written_content)

    # Check for correct inventory structure and IP sorting
    hosts: dict[str, Any] = output_inventory["all"]["hosts"]
    host_names: list[str] = list(hosts.keys())

    assert host_names == ["web01", "web02"]
    assert hosts["web01"]["ansible_host"] == "192.168.1.2"

    # Verify Ansible module exit call
    mock_module_instance.exit_json.assert_called_once()
