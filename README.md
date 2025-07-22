# Shigahochi RSS

This repository builds an RSS feed for the [Shigahochi Newspaper](http://www.shigahochi.co.jp/).
A GitHub Actions workflow scrapes article links from the site's front page and commits
`rss.xml` back into this repository. You can subscribe to the RSS file with any reader
(such as Feedly) to receive updates automatically.

## Workflow Overview

The workflow `.github/workflows/rss-generator.yml` runs daily and can also be triggered
manually. It executes `rss_generator.py` to fetch the latest articles and commits the
resulting `rss.xml` if there are changes.

The script relies only on Python's standard library, so you can run it locally
with `python rss_generator.py` without installing extra packages.
The fetch request now includes a simple `User-Agent` header to avoid being
rejected by the server. If you still encounter HTTP 403 errors, your network or
the site may be blocking access.

## Using the Feed

1. Navigate to the repository's `rss.xml` file.
2. Copy the raw file URL (e.g., `https://raw.githubusercontent.com/<user>/<repo>/main/rss.xml`).
3. Add that URL to your RSS reader such as Feedly.

The feed will update automatically when the workflow runs.
