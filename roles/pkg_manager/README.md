# Package Manager

A universal, cross-platform package manager role for Ansible. It simplifies installations by automatically switching between `apt`, `dnf`, `pacman`, and `package` based on the target OS, while handling both repository packages and local file paths (like `.deb`, `.rpm`, or `.pkg.tar.*`) seamlessly.

## Features

* **OS Autodetection**: Automatically uses the correct module for Debian/Ubuntu, RedHat/Fedora, and Arch Linux with a generic fallback.
* **Unified Advanced Removal**: Standardizes advanced package cleanups like purging config files and autoremoving orphaned dependencies across all platforms.
* **Zero-Loop Batching**: Passes package lists directly to native package managers in a single action for massive performance gains.
* **Isolated File Support**: Automatically splits and safely loops over local file installations (`.deb`, `.rpm`, `.pkg.tar.*`) using dedicated `package` loops to prevent parameter pollution.
* **Argument Validation**: Enforces exact structural types and safe variable coersion at runtime using native `meta/argument_specs.yml`.

## Role Variables

The following variables are defined in `meta/argument_specs.yml` and can be passed to the role:

| Variable | Type | Required | Default | Choices | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pkg_manager_pkgs` | list | Yes | `[]` | N/A | List of package names or full paths/URLs to local package files. Single string values will auto-coerce to a list. |
| `pkg_manager_state` | str | No | `present` | `present`, `absent`, `latest` | Target state of the packages. |
| `pkg_manager_remove_level` | str | No | `standard` | `standard`, `purge`, `autoremove`, `complete` | Cleanup strategy used *only* when `pkg_manager_state` is set to `absent`. |
| `pkg_manager_update_cache` | bool | No | `true` | `true`, `false` | Whether to update repository metadata before executing standard package operations. |
| `pkg_manager_verbose` | bool | No | `false` | `true`, `false` | Toggle verbose operations and customized logging flags. |

### Understanding Removal Levels (`pkg_manager_state: absent`)

| Level | Debian/Ubuntu (`apt`) | Red Hat/Fedora (`dnf`) | Arch Linux (`pacman`) | Fallback (`package`) |
| :--- | :--- | :--- | :--- | :--- |
| **`standard`** | Removes package binaries only. | Removes package & configurations. | Removes package binaries only. | Standard removal fallback. |
| **`purge`** | Removes package & config files. | Removes package & configurations. | Drops configuration backup flags (`-Rn`). | Standard removal fallback. |
| **`autoremove`** | Removes package & unused dependencies. | Removes package & unused dependencies. | Recursively strips unused dependencies (`-Rs`). | Standard removal fallback. |
| **`complete`** | Purges package, configurations, & dependencies. | Removes package & unused dependencies. | Recursively strips dependencies & backups (`-Rns`). | Standard removal fallback. |

## Example Usage

You can call this role directly from a playbook or as an embedded inclusion layer inside other complex collection components.

### Single Package Install

```yaml
- name: Install Vim
  ansible.builtin.include_role:
    name: jcook3701.utils.pkg_manager
  vars:
    pkg_manager_pkgs: ["vim"]
```

### Local File Install (e.g., Google Chrome)

```yaml
- name: Install Google Chrome from local file
  ansible.builtin.include_role:
    name: jcook3701.utils.pkg_manager
  vars:
    pkg_manager_pkgs: ["/tmp/google-chrome-stable_current_amd64.deb"]
    pkg_manager_update_cache: false
```

### Advanced System/Package Cleanup

```yaml
- name: Wreak havoc and purge all traces of Apache
  ansible.builtin.include_role:
    name: jcook3701.utils.pkg_manager
  vars:
    pkg_manager_pkgs: ["apache2"]
    pkg_manager_state: "absent"
    pkg_manager_remove_level: "complete"
```

### Multi-Package Mixture (Repositories and Files)

```yaml
- name: Setup Multi-Source Workstation Environment
  ansible.builtin.include_role:
    name: jcook3701.utils.pkg_manager
  vars:
    pkg_manager_pkgs:
      - xfce4
      - xfce4-goodies
      - git
      - "/tmp/custom-enterprise-agent.rpm"
    pkg_manager_state: "latest"
```

## Requirements

* **community.general** collection (required for **pacman** module support on Arch Linux targets).

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
