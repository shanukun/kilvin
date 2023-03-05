# kilvin

kilvin is a minimal static site generator.

- Minimal templating language
- Minimal config with support for custom variables.
- Automatic table of contents generation
- Dynamic menu creation
- TOML, YAML, and JSON metadata support in front matter


## Install

```console
pip install kilvin
```


## Usage

<!-- Find the documentation for the usage here: [Documentation](https://www.github.com/shanukun/kilvin) -->

### Create project

```console
kilvin init <project name>
```

### Add page to project

```console
kilvin new pages/post.md
```

`content/pages/post.md` will be created.

After that:
```console
kilvin build
```
All the markdown pages will be rendered to HTML and will be saved in `public` directory.

To view the rendered website use:
```console
kilvin server
```

## Configuration

Configure site using `config.toml` file.
Basic Config:
```
title = 'My Blog'
url = "https://myblog.xyb"
description = 'My corner of the internet.'

[author]
    name = "Shanu"
    email = "shanu@myblog.xyb"
```


## Directory Tree

```
project
|-- public
|-- content
|   └── blog.md
|-- static
|-- layouts
    └── text.html
```


### Content

`_index.md` allows you to add front matter and content for list templates.


```
└── content
    └── about
    |   └── _index.md
    ├── posts
    |   └── _index.md
    |   ├── firstpost.md
    |   ├── happy
    |   |   └── ness.md
    |   └── secondpost.md
    └── quote
    |   └── _index.md
        ├── first.md
        └── second.md
```

## Templating

kilvin uses Jinaj2 templating as the basis for templating. All the template files should be placed in `layout/` directory.
A basic example would be:

```
<html>
    <head>
        <title> {{ meta.title }} </title>
    </head>

    <body>
        {{ body }}
    </body>

    <footer>
        {{ footer }}
    </footer>
</html>
```

### Front Matter

kilvin allows to add front matter in yaml, toml, or json to your content file.

Example:
```
---
template: foo.html
title: Why does it ended?
subtitle: It has not just joking
date: 2022-28-09
---

[TOC]

## markdown here
...
```

`layout` directory must have `single.md` and `list.md` as the default templates.

Non-index templates have access to the below objects:
- site: date in config.toml
- meta: data from the front matter
- body: html content of the page

Index template (for `_index.md`) have access to everything above, and `pages` and `dirs` objects,
which is a list containing HTML and front matter of pages. 



## Feeds

Atom feeds are generated for all the directories under `content`. So `content/bar` will have
a Atom feed at `public/bar/feed.xml`.
