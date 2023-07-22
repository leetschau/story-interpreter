from datetime import date


def qmd_header(title: str) -> str:
    return f"""---
title: {title.title()}
author:
- Leo
date: {date.today()}
toc: true
toc-depth: 3
number-sections: false
format:
  html:
    embed-resources: true
  epub:
    standalone: true
    epub-title-page: false
---
"""

