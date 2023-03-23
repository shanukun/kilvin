![python](https://img.shields.io/badge/Python-v3.9.2-blue)
![mit](https://img.shields.io/badge/license-MIT-9cf)
![linux](https://img.shields.io/badge/platform-linux-ffd)

# kilvin

Kilvin is a simple static site generator. It takes markdown text and turns it 
into a static webpage using layouts. Changes can be made to the page's content, 
URLs, and the way the site looks.

- Minimal templating language
- Minimal config with support for custom variables
- Automatic table of contents generation


## Getting Started

### Prerequisites

Kilvin requires the following:

- Python version 3.9 or higher
- pip : package installer


### Instructions

1. Install all prerequisites.
1. Install the `kilvin`.

```console
$ pip install kilvin
```
### Create a site

1. Create a new kilvin site at `./my_project`

```console
$ kilvin init my_project
```
2. Change into your new directory.

```console
$ cd my_project
```
3. Build the site.

```console
$ kilvin build
```
4. Make it available on local server.

```console
$ kilvin server
```

## Command Line

Kilvin has several commands:

```
Usage: kilvin [OPTIONS] COMMAND [ARGS]...

  Kilvin is a simple static site generator. It takes markdown text and turns
  it into a static webpage using layouts.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  build   Build the current project
  init    Create directory structure for the project
  new     Create a new markdow post in ./content dir
  server  Serve the current project
```

Here are some of the most common command:

- `kilvin init PATH`: 
    - Create a new kilvin site with requisite directory structure.

- `kilvin new PATH`: 
    - Help create new markdown pages for the project.
    - All the new pages are stored in content directory.
    - Example:

        For `content/about.md`

        ```console
        $ kilvin new about.md
        ```

        For `content/blog/today.md`

        ```console
        $ kilvin new blog/today.md
        ```

- `kilvin build`:
    - Build the site from `./content` files using template in `./layout` and save them `./public` directory.
    - All the non-markdown files in `./content` are copied directly without any changes.
    - `./static` is also directly copied to `./public`.

- `kilvin server`:
    - Serves the site locally.


## Config

Edit `config.toml` for changing the configuration for the project. 

### Default Configuration

Basic configuration required for building the site.

```
title = 'My Blog'
url = "https://myblog.xyb"
description = 'My corner of the internet.'

[author]
name = "Kilvin"
email = "kilvin@myblog.xyb"
```

#### Custom Configuration

Custom variables can also be defined in `config.toml`.

```
var1 = 123

[name1]
var2 = "abcxyz"
var3 = 123
```

All the variables in `config.toml` can be accessed in HTML templates with `site` variable.
Example:

- `{{ site.title }}`
- `{{ site.author.name }}`
- `{{ site.name1.var2 }}`


## Pages & Layouts

kilvin organize the rendered site in the same structure that is used to organize the 
source conent.

```
└── content
    └── about.md
    ├── posts
    |   └── _index.md
    |   ├── firstpost.md
    |   └── secondpost.md
    └── quote
        └── _index.md
        ├── first.md
        └── second.md
```

```
└── public
    └── about
    |   └── index.html
    ├── posts
    |   └── index.html
    |   ├── firstpost
    |   |   └── index.html
    |   └── secondpost
    |   |   └── index.html
    └── quote
        └── index.html
        ├── first
            └── index.html
        └── second
            └── index.html
```

### Pages

- All markdown files are referred as a Pages.

### Creating a Page

- To create a page, add a markdown file to `./content` directory.
- Pages can also be organized in sub directories, and all sub directories should have a 
`_index.md` page.

- All pages must have a front matter, enclosed in `---` which is used to specify the template or other meta data, along with custom data.

    Example:

    ```markdown
    ---
    template: single.html
    title: Why does it have to end?
    subtile: A survivor dies.
    date: 2022-28-09
    ---

    [TOC]
    

    markdown here
    ```

    - `template`, `tilte`, `subtitle` and `date` are mandatory.
    - If `template` field is empty, then default templates are used.

- All the variables can be accessed using `meta` variable in template.

    - Example

        - `{{ meta.title }}`
        - `{{ meta.subtitle }}`
        - `{{ meta.date }}`

### Index Page

- All the directories should have `_index.md` page.
- Index Page is special as it has access to variable `pages`.


### Layout

- kilvin uses Jinja2 for templating.
- `./layout` contains the templates for the Pages.
- `./layout` should have `list.html` and `single.html` as the default templates.

#### Variables

All the templates have access to a bunch of variables.

- `site`: date in `config.toml`
- `meta`: data from front matter of the page
- `body`: rendered markdown from the page
- `pages`: (only available to index template) list of all the page in directory

#### Template Usage

```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ site.title }}</title>
    <link rel="stylesheet" href="/static/style.css">
  </head>
  <body>
    <nav>
      <a href="/">Home</a>
      <a href="/blog/">Blog</a>
    </nav>
    <h1>{{ meta.title }}</h1>
    <section>
      {{ body }}
    </section>
  </body>
</html>
