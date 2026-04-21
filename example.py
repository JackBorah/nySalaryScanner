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