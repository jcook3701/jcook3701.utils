# Autobuild

To avoid linting errors, prefix your variables in your role's `vars/` and map them when calling this routine:

``` yaml
- include_role:
    name: jcook3701.utils.autobuild
    task_from: pkg-source-build-init-routine.yml
  vars:
    git_repo: "{{ myrole_git_repo }}"
    build: "{{ myrole_build }}"
    name: "{{ myrole_name }}"
```
