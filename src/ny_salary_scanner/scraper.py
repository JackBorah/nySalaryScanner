from typing import List

from playwright.sync_api import Playwright, sync_playwright, expect

def scrape(
        headless: bool = False,
        names: list[str] = [],
        years: List[int] = [],
        branches: list[str] = [],
        agencies: List[str] = [],
        sub_agencies: List[str] = [],
        titles: List[str] = [],
        min_pay: int = 0,
        max_pay: int = 0,
        sort_by: str = '',
        timeout: int = 1000, # ms
        outputHTML: str = "ScrapedSeeThroughNy.html"
        ) -> None:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(10000)
    page.goto("https://www.seethroughny.net/payrolls")
    page.locator("[id^='stny_payYear_']").get_by_text("x", exact=True).click() # removes checked default
    page.get_by_text("x", exact=True).click()
    page.locator("#stny_sortBy00").get_by_text("x", exact=True).click()

    if (names):
        page.get_by_role("link", name=" Name").click()
        for name in names:
            page.get_by_role("textbox", name="Last, First").click()
            page.get_by_role("textbox", name="Last, First").fill(name)
            page.get_by_role("textbox", name="Last, First").press("Enter")

    if (years):
        page.get_by_role("link", name=" Year").click()
        for year in years:
            page.get_by_role("listitem").filter(has_text=str(year)).click()
   
    if (branches):
        page.get_by_role("link", name=" Branch/Major Category").click()
        for branch in branches:
            page.get_by_label("Payrolls").get_by_role("listitem").filter(has_text=branch).click()

    if (agencies):
        page.get_by_role("link", name=" Employer/Agency").click()
        for agency in agencies:
            page.get_by_role("tabpanel", name=" Employer/Agency").get_by_placeholder("Search").click()
            page.get_by_role("tabpanel", name=" Employer/Agency").get_by_placeholder("Search").fill(agency)
            page.get_by_role("tabpanel", name=" Employer/Agency").get_by_placeholder("Search").press("Enter")
            
            page.locator("#agencyGroup > .list-group > li > .check").click()

    # SubAgency has a specific name you will have to find on SeeThroughNY.
    # SUC@Old Westbury or SUCOld Westbury for example.
    if (sub_agencies):
        page.get_by_role("link", name=" SubAgency/Type").click()
        for sub in sub_agencies:
            page.get_by_role("tabpanel", name=" SubAgency/Type").get_by_placeholder("Search").click()
            page.get_by_role("tabpanel", name=" SubAgency/Type").get_by_placeholder("Search").fill(sub)

            page.locator("#subagencyGroup > .list-group > li > .check").click()
    
    if (titles):
        page.get_by_role("link", name=" Title").click()
        for title in titles:
            page.locator("#positionNameGroup").get_by_role("textbox", name="Search").click()
            page.locator("#positionNameGroup").get_by_role("textbox", name="Search").fill(title)
            page.locator("#positionNameGroup").get_by_role("textbox", name="Search").press("Enter")
            page.get_by_label("Payrolls").get_by_text(title, exact=True).click()

    # TODO Fix this
    # if (min_pay, max_pay):
    #     page.get_by_role("link", name=" Total Pay").click()
    #     page.locator(".slider-range")
    #     page.evaluate("""
    #         (min_pay, max_pay) => {
    #             const min_input = document.querySelector('#ytdPayGroup > p > input[type=hidden]:nth-child(2)');
    #             const max_input = document.querySelector('#ytdPayGroup > p > input[type=hidden]:nth-child(3)');
    #             min_input.value = min_pay;
    #             max_input.value = max_pay;
    #         }
    #     """)

    if (sort_by):
        page.get_by_role("link", name=" Sort By").click()
        page.locator("#SortBy-button").get_by_text("Select a value").click()
        page.get_by_role("option", name=sort_by).click()

    page.get_by_role("link", name="Search").click()

    try:
        page.get_by_text("Load More Results").wait_for(state="visible", timeout=3000)
        while (page.get_by_text("Load More Results").is_visible()):
            page.wait_for_timeout(timeout)
            page.get_by_text("Load More Results").click()
            page.wait_for_timeout(timeout)
    except:
        pass
    results = page.locator("#tbl_results").inner_html()

    with open(outputHTML, "w") as f:
        f.write(results)

    context.close()
    browser.close()
    playwright.stop()

# if __name__ == "__main__":
#     # Just picked the highest paid person from 2025. Its arbitrary for testing.
#     scrape(
#         names=["Johnson, Phd Candace S"],
#         years = [2025],
#         branches = ["Public Authorities"],
#         agencies = ["Roswell Park Cancer Institute Corporation"],
#         sub_agencies = ["Roswell Park Cancer Institute Corporation"],
#         titles = ["President & Ceo"],
#         min_pay = 100,
#         max_pay = 3000000,
#         sort_by = 'Name',
#         timeout = 1000, # ms
#         outputHTML = "output.html"
#         )