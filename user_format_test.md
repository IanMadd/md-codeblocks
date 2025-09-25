+++
title = "docker_plugin resource"
draft = false

platform = "linux"

[menu.resources]
    title = "docker_plugin"
    identifier = "resources/core/docker_plugin.md docker_plugin resource"
    parent = "resources/core"
+++

# Docker Plugin Resource Test

This file tests the exact frontmatter format you specified.

## Code Example

Here's some example code:

```
resource "docker_plugin" "example" {
  name = "test/plugin:latest"
  enabled = true
}

output "plugin_id" {
  value = docker_plugin.example.id
}
```

## More Content

Regular markdown content continues here.