# Container Engine

Ansible utility role used to manage decoupled container composition environments and runtime engines.

## Overview

This role abstracts container composition mechanics away from application roles. It provides an isolated framework to synchronize target infrastructure lifecycle states natively across Docker Compose v2 or Podman Compose stacks.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| **container_engine_project_src** | str | The absolute host filesystem directory path containing the targeted composition infrastructure deployment file setup configuration layer. | `"/opt/container-stack"` |
| **container_engine_platform_type** | str | The targeted underlying context engine preference tool metric selecting active processing daemon runtime environment layers downstream. <br> Choices: `docker`, `podman` | `"docker"` |
| **container_engine_desired_state** | str | Deployment lifecycles baseline profile enforcement parameter managing creation hooks, container stack removal, or complete data purge actions. <br> Choices: `present`, `absent`, `teardown` | `"present"` |
| **container_engine_trigger_condition** | bool | Metric gate tracking validation conditional criteria evaluated explicitly before triggering engine execution modifications on systems. | `true` |
| **container_engine_pull_images** | bool | Control tracking boolean flag forcing layer registry synchronization lookup sweeps to pull images down to local nodes during initialization cycles. | `true` |

## Requirements

The following collections must be available in the execution environment to leverage their respective module runtimes:

* `community.docker`
* `containers.podman`

## Usage Examples

### Example 1: Deploying a Stack via Docker Compose

```yaml
- name: Bring up application services
  ansible.builtin.import_role:
    name: jcook3701.utils.container_engine
  vars:
    container_engine_project_src: "/opt/my-app"
    container_engine_platform_type: "docker"
    container_engine_desired_state: "present"
    container_engine_trigger_condition: true
```

### Example 2: Tearing Down a Stack via Podman Compose

```yaml
- name: Purge application stack containers
  ansible.builtin.import_role:
    name: jcook3701.utils.container_engine
  vars:
    container_engine_project_src: "/opt/my-app"
    container_engine_platform_type: "podman"
    container_engine_desired_state: "teardown"
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
