---
template:
title: Command Line Usage
subtitle: 
date: 2023-03-11
draft: True
---

Kilvin has several commands:

```
usage: kilvin [-h] [init,build,server,new] ...

A simple static site generator.

positional arguments:
  {init,build,server,new}
                        Help:
    init                Create directory structure for the project.
    new                 Create a new markdow post.
    build               Build the current project.
    server              Serve the current project.

optional arguments:
  -h, --help            show this help message and exit


```
Here are some of the most common command:

- `kilvin init PATH`: 
    - Create a new kilvin site with requisite directory structure.

- `kilvin new PATH`: 
    - Help create new markdown pages for the project.
    - All the new pages are stored in content directory.
    - Example:

        For `content/about.md`

        ```
        kilvin new about.md
        ```

        For `content/blog/today.md`

        ```
        kilvin new blog/today.md
        ```

- `kilvin build`:
    - Build the site from `./content` files using template in `./layout` and save them `./public` directory.
    - All the non-markdown files in `./content` are copied directly without any changes.
    - `./static` is also directly copied to `./public`.

- `kilvin server`:
    - Serves the site locally.
