+++
title = "docker_plugin resource"
draft = false

platform = "linux"

[menu.resources]
    title = "docker_plugin"
    identifier = "resources/core/docker_plugin.md docker_plugin resource"
    parent = "resources/core"
+++

# Docker Plugin Resource

This is a sample markdown file with frontmatter and indented code blocks.

## Example Usage

Here's how to use the docker plugin:

```
resource "docker_plugin" "sample" {
  name                  = "vieux/sshfs:latest"
  alias                 = "sshfs"
  enabled               = false
  grant_all_permissions = true
  
  env = [
    "DEBUG=1"
  ]
}
```

## Configuration Options

The following options are available:

```
# Enable the plugin
enabled = true

# Grant permissions
grant_all_permissions = false
```

That's the basic configuration.