from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.seethroughny.net/payrolls")
    page.locator("#stny_payYear_2025").get_by_text("x", exact=True).click()
    page.get_by_text("x", exact=True).click()
    page.get_by_role("link", name=" SubAgency/Type").click()
    page.get_by_role("textbox", name="Search").click()
    page.get_by_role("textbox", name="Search").fill("farm")
    page.get_by_role("textbox", name="Search").fill("westbury")

    # page.get_by_text("Farmingdale State").click()
    page.get_by_text("SUC@Old Westbury").click()
    page.get_by_text("SUCOld Westbury").click()
    page.get_by_role("link", name=" Year").click()

    while (page.get_by_text("Load More Results").is_visible()):
        page.wait_for_timeout(2000)
        page.get_by_text("Load More Results").click()
        page.wait_for_timeout(2000)
    results = page.locator("#tbl_results").inner_html()
    with open("westbury_results.html", "w") as f:
        f.write(results)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
