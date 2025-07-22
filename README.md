# Shigahochi RSS

This repository automatically builds an RSS feed for the [Shigahochi Newspaper](http://www.shigahochi.co.jp/). The feed contains links scraped from the site's front page and can be consumed by any RSS reader.

## Workflow

A GitHub Actions workflow located in `.github/workflows/rss-generator.yml` performs the scraping. It runs on a daily schedule and can also be triggered manually.

- **Schedule:** `10 1 * * *` (10:10 JST every day)
- **Manual Run:** via the `workflow_dispatch` event on GitHub

The workflow scrapes article links, compiles them into an RSS document and commits the result back to this repository.

## Output

The generated RSS file is committed as `rss.xml` in the repository root. This file is updated each time the workflow runs.
