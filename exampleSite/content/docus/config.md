---
template:
title: Configuration
subtitle: 
date: 2023-03-11
draft: True
---

[TOC]

Edit `config.toml` for changing the configuration for the project. 

## Default Configuration

Basic configuration required for building the site.
```
title = 'My Blog'
url = "https://myblog.xyb"
description = 'My corner of the internet.'

[author]
name = "Kilvin"
email = "kilvin@myblog.xyb"
```

### Custom Configuration

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
