import pytest

import config
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config.playwright import Playwright #
from config.expectations import Expectations #

@pytest.fixture()
def page() -> Page:
    playwright = sync_playwright().start()
    if Playwright.BROWSER == 'firefox':
        browser = get_firefox_browser(playwright)
        context = get_context(browser)
        page_data = context.new_page()
    elif Playwright.BROWSER == 'chrome':
        browser = get_chrome_browser(playwright)
        context = get_context(browser)
        page_data = context.new_page()
    else:
        browser = get_chrome_browser(playwright)
        context = get_context(browser)
        page_data = context.new_page()
    yield page_data
    for context in browser.contexts:
        context.close()
    browser.close()
    playwright.stop()


def get_firefox_browser(playwright) -> Browser:
    return playwright.firefox.launch(
        headless=config.playwright.Playwright.IS_HEADLESS,
        slow_mo=config.playwright.Playwright.SLOW_MO,
    )


def get_chrome_browser(playwright) -> Browser:
    return playwright.chromium.launch(
        headless=config.playwright.Playwright.IS_HEADLESS,
        slow_mo=config.playwright.Playwright.SLOW_MO
    )


def get_context(browser) -> BrowserContext:
    context = browser.new_context(
        viewport=config.playwright.Playwright.PAGE_VIEWPORT_SIZE,
        locale=config.playwright.Playwright.LOCALE
    )
    context.set_default_timeout(
        # timeout=config.expectations.Expectations.DEFAULT_TIMEOUT
        timeout=Expectations.DEFAULT_TIMEOUT

    )
    return context
