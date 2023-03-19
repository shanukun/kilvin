---
template:
title: Pages & Layout
subtitle:
date: 2023-03-09
draft: True
---


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

## Pages

- All markdown files are referred as a Pages.

## Creating a Page

- To create a page, add a markdown file to `./content` directory.
- Pages can also be organized in sub directories, and all sub directories should have a 
`_index.md` page.

- All pages must have a front matter, enclosed in `---` which is used to specify the template or other meta data, along with custom data.

    Example:

    <div>
    <p>---</p>
    <p>template: single.html</p>
    <p>title: Why does it have to end?</p>
    <p>subtile: A survivor dies.</p>
    <p>date: 2022-28-09</p>
    <p>---</p>

    <p>[TOC]</p>
    

    <p>markdown here</p>
    </div>

    - `template`, `tilte`, `subtitle` and `date` are mandatory.
    - If `template` field is empty, then default templates are used.

- All the variables can be accessed using `meta` variable in template.

    - Example

        - `{{ meta.title }}`
        - `{{ meta.subtitle }}`
        - `{{ meta.date }}`

## Index Page

- All the directories should have `_index.md` page.
- Index Page is special as it has access to variable `pages`.


## Layout

- kilvin uses Jinj2 for templating.
- `./layout` contains the templates for the Pages.
- `./layout` should have `list.html` and `single.html` as the default templates.

### Variables

All the templates have access to a bunch of variables.

- `site`: date in `config.toml`
- `meta`: data from front matter of the page
- `body`: rendered markdown from the page
- `pages`: (only available to index template) list of all the page in directory

### Usage

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

```







