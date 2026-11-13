# Utilities

## Package Facts

Gater facts from all hosts and tests if important packages have been installed.

``` shell
$ ansible-playbook package-facts-all.yml
```

## Ansible Examples

**Example A:** Run a single specific task cleanly

``` shell
- name: Collect package details across nodes
  ansible.builtin.include_role:
    name: jcook3701.utils.general
  vars:
    general_task_action: "package_facts"
```

**Example B:** Chain multiple tasks together using the flags

``` shell
- name: Clean up apt and reload configuration
  ansible.builtin.include_role:
    name: jcook3701.utils.general
  vars:
    general_enable_apt_clean: true
    general_enable_reload_shell: true
```
