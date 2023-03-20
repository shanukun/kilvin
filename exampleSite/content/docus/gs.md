---
template:
title: Getting Started
subtitle: 
date: 2023-03-09
draft: True
---

Kilvin is a simple static site generator. It takes markdown text and turns it 
into a static webpage using layouts. Changes can be made to the page's content, 
URLs, and the way the site looks.


## Prerequisites

Kilvin requires the following:

- Python version 3.9 or higher
- pip : package installer


## Instructions

1. Install all prerequisites.
1. Install the `kilvin`.
```
pip install kilvin
```
## Create a site

1. Create a new kilvin site at `./my_project`
```
kilvin init my_project
```
2. Change into your new directory.
```
cd my_project
```
3. Build the site.
```
kilvin build
```
4. Make it available on local server.
```
kilvin server
```



