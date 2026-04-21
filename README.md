# NY Salary Scanner
A library that synchronously scrapes and downloads salary data from [seethroughny.net](https://seethroughny.net/) in a csv format.

## Installation
    pip install ny-salary-scanner==0.0.1 

## Example
    from ny_salary_scanner import scraper, parser

    html_output = "output.html"

    scraper.scrape(
            names=["Johnson, Phd Candace S"],
            years = [2025],
            branches = ["Public Authorities"],
            agencies = ["Roswell Park Cancer Institute Corporation"],
            sub_agencies = ["Roswell Park Cancer Institute Corporation"],
            titles = ["President & Ceo"],
            # min_pay = 100, # Not currently supported
            # max_pay = 3000000, # Not currently supported
            sort_by = 'Name',
            timeout = 1000, # ms
            outputHTML = html_output
        )

parser.parse(html_output) # the cwd will contain salaries.csv and output.html after running

## Workflow
Playwright opens chrome and searches using the provided parameters. Then, it will click "Load More Results" repeatedly until there is no additional data to load. This step is throttled to be respectful to the website. Now the HTML is saved and downloaded where it will be parsed by BeautifulSoup4 and saved as a CSV.

## Technology
- Playwright
- BeautifulSoup4
- Python
