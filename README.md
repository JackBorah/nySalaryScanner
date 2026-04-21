# NY Salary Scanner
A library that synchronously scrapes and downloads salary data from [seethroughny.net](https://seethroughny.net/) in a csv format.

## Example


## Workflow
Playwright opens chrome and searches using the provided parameters. Then, it will click "Load More Results" repeatedly until there is no additional data to load. This step is throttled to be respectful to the website. Now the HTML is saved and downloaded where it will be parsed by BeautifulSoup4 and saved as a CSV.

## Technology
- Playwright
- BeautifulSoup4
- Python
