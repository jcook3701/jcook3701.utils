# Package Manager

A universal, cross-platform package manager role for Ansible. It simplifies installations by automatically switching between `apt`, `dnf`, `pacman`, and `package` based on the target OS, while handling both repository packages and local file paths (like `.deb` or `.rpm`) seamlessly.

## Features

* **OS Autodetection**: Automatically uses the correct module for Debian/Ubuntu, RedHat/CentOS, and Arch Linux.
* **Smart Install**: Automatically detects file extensions; uses the `deb` parameter for `.deb` files on Debian-based systems.
* **Argument Validation**: Uses `argument_specs` to ensure variables are correctly formatted before any tasks run.
* **Standardized API**: Provides a consistent interface for all your other collection roles to call.

## Role Variables

The following variables are defined in `meta/argument_specs.yml` and can be passed to the role:

| Variable | Type | Required | Default | Choices | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pkg_manager_pkgs` | list | Yes | `[]` | N/A | List of package names or full paths to local `.deb`/`.rpm` files. |
| `pkg_manager_state` | str | No | `present` | `present`, `absent` | Whether the packages should be installed or removed. |
| `pkg_manager_update_cache` | bool | No | `true` | `true`, `false` | Whether to update the repository metadata before installing. |

## Example Usage

You can call this role directly from a playbook or as a nested include within another role.

### Single Package Install

``` yaml
- name: Install Vim
  ansible.builtin.include_role:
    name: jcook3701.utils.package_manager
  vars:
    pkg_manager_pkgs: ["vim"]
```

### Local File Install (e.g., Google Chrome)

``` yaml
- name: Install Google Chrome from local file
  ansible.builtin.include_role:
    name: jcook3701.utils.package_manager
  vars:
    pkg_manager_pkgs: ["/tmp/google-chrome-stable_current_amd64.deb"]
    pkg_manager_update_cache: false
```

### Multi-Package List

``` yaml
- name: Setup Workstation Environment
  ansible.builtin.include_role:
    name: jcook3701.utils.package_manager
  vars:
    pkg_manager_pkgs:
      - xfce4
      - xfce4-goodies
      - git
      - curl
    pkg_manager_state: "present"
```

## Requirements

* **community.general*** collection (required for **pacman** module support).
