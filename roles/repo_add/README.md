# Repository Add (`repo_add`)

**repo_add** is a generic utility role designed to safely manage cross-platform repositories. It dynamically configures native repository definitions across Debian, Red Hat, and Arch Linux systems using modern package management standards.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`repo_add_id`** | The unique shorthand identifier used for the repository filename and INI configuration block headers. | *Required* |
| **`repo_add_name`** | The descriptive, human-readable name assigned to the repository. | *Required* |
| **`repo_add_enabled`** | Determines whether the repository index is actively checked by the system package manager. | `true` |
| **`repo_add_state`** | The targeted lifecycle execution state. Set to `absent` to cleanly purge the repository files from the OS. | `"present"` |
| **`repo_add_debian_types`** | The types of packages to fetch for Debian/Ubuntu systems (e.g., `deb`, `deb-src`). | `"deb"` |
| **`repo_add_debian_uris`** | The base distribution package download URL for Debian/Ubuntu systems. | `""` |
| **`repo_add_debian_suites`** | The specific distribution release codename (e.g., bookworm, jammy). | `""` |
| **`repo_add_debian_components`** | The repository sections to track (e.g., main, stable, contrib). | `""` |
| **`repo_add_debian_signed_by`** | An HTTPS web URL or local file path pointing to the cryptographic validation GPG key. | `""` |
| **`repo_add_redhat_baseurl`** | The upstream mirror URL pointing to the standard RPM package directory tree. | `""` |
| **`repo_add_redhat_gpgkey`** | An HTTPS web URL or local file path pointing to the repository's cryptographic GPG verification key. | `""` |
| **`repo_add_arch_sig_level`** | Cryptographic signature trust and verification requirements for this specific Arch Linux pacman repository block. | `""` |
| **`repo_add_arch_server`** | The remote server path hosting package databases for pacman configuration files. | `""` |

## Supported Topologies

The utility interprets the underlying target operating system using Ansible system facts and executes the corresponding platform-specific implementation:

* **Debian / Ubuntu:** Provisions decoupled, modern DEB822 source sheets under `/etc/apt/sources.list.d/` and dynamically tracks GPG signatures in `/etc/apt/keyrings/`.
* **Red Hat / Enterprise Linux:** Renders standardized `.repo` files compatible with `dnf`/`yum` inside `/etc/yum.repos.d/`.
* **Arch Linux:** Dynamically appends or removes structural repository server mirrors and signature thresholds within `/etc/pacman.conf`.

## Example Playbooks

### 1. Adding a Debian/Ubuntu Repository (e.g., Docker CE)

```yaml
- name: Install Remote Package Repositories
  hosts: debian_nodes
  become: true
  tasks:
    - name: Dynamically Provision Docker CE Repository
      ansible.builtin.include_role:
        name: jcook3701.utils.repo_add
      vars:
        repo_add_id: "docker-ce"
        repo_add_name: "Docker Community Edition"
        repo_add_debian_uris: "https://docker.com"
        repo_add_debian_suites: "{{ ansible_distribution_release }}"
        repo_add_debian_components: "stable"
        repo_add_debian_signed_by: "https://docker.com/gpg"
```

### 2. Adding a Red Hat Enterprise Linux Repository

```yaml
- name: Install Remote Package Repositories
  hosts: rhel_nodes
  become: true
  tasks:
    - name: Dynamically Provision Rocky Linux BaseOS Repository
      ansible.builtin.include_role:
        name: jcook3701.utils.repo_add
      vars:
        repo_add_id: "rocky-baseos"
        repo_add_name: "Rocky Linux BaseOS Upstream Mirror"
        repo_add_redhat_baseurl: "https://rockylinux.org"
        repo_add_redhat_gpgkey: "https://rockylinux.org"
```

### 3. Decommissioning / Removing a Repository Completely

```yaml
- name: Purge Obsolete Infrastructure Repositories
  hosts: all
  become: true
  tasks:
    - name: Safely Delete Legacy Repository Definitions and Tracking Keys
      ansible.builtin.include_role:
        name: jcook3701.utils.repo_add
      vars:
        repo_add_id: "legacy-custom-repo"
        repo_add_name: "Obsolete Share Point"
        repo_add_state: "absent"
```

---

## Author Information

Maintained by **Jared Cook** as a central component of the automation infrastructure layout.
