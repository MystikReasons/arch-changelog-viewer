from typing import Optional, Dict, Any, List
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
from bs4 import BeautifulSoup
import requests


class WebScraper:
    def __init__(self, logger, config: Optional[Dict[str, Any]]) -> None:
        """Constructor method"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.logger = logger
        self.config = config

    def fetch_page_content(self, url: str, retries: int = 3) -> Optional[str]:
        """Fetches the full HTML content of a page using Playwright with retry logic.

        Creates a new browser context and navigates to the given URL.
        Retries the request on timeout or other errors, up to the specified number of attempts.

        :param url: The target URL to fetch content from.
        :type url: str
        :param retries: Number of retry attempts in case of failure.
        :type retries: int
        :return: HTML content of the page as a string, or None if all attempts fail.
        :rtype: Optional[str]
        """
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
        )

        attempt = 0
        while attempt < retries:
            try:
                context = self.browser.new_context(
                    locale="en-US", user_agent=user_agent
                )

                page = context.new_page()
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle", timeout=60000)
                content = page.content()
                return content
            except TimeoutError:
                self.logger.error(
                    f"[Error]: Timeout error while fetching {url}. Retrying... [{attempt+1}/{retries}]"
                )
            except Exception as ex:
                self.logger.error(
                    f"[Error]: Error while fetching {url}: {ex}. Retrying... [{attempt+1}/{retries}]"
                )
            finally:
                attempt += 1
                if attempt < retries:
                    if page:
                        page.wait_for_timeout(
                            self.config.config.get("webscraper-delay")
                        )
                        page.close()
                else:
                    page.close()

        self.logger.error(
            f"[Error]: Failed to fetch content from {url} after {retries} retries."
        )
        return None

    def find_all_elements(
        self, content: str, tag: Optional[str] = None, **kwargs: Any
    ) -> List:
        """Finds all elements in the HTML content based on the specified tag and additional attributes.

        :param content: The HTML content to be parsed.
        :type content: str
        :param tag: The HTML tag that is being searched for (e.g. 'p', 'span', etc.).
        :type tag: Optional[str]
        :param kwargs: Additional attributes that are searched for (e.g. class_, id, attrs, etc.).
        :type kwargs: Any
        :return: A list of matched elements.
        :rtype: List
        """
        soup = BeautifulSoup(content, "html.parser")
        return soup.find_all(tag, **kwargs)

    def find_element(
        self, content: str, tag: Optional[str] = None, **kwargs: Any
    ) -> Optional:
        """Finds an element in the HTML content based on the specified tag and additional attributes.

        :param content: The HTML content to be parsed.
        :type content: str
        :param tag: The HTML tag that is being searched for (e.g. 'p', 'span', etc.).
        :type tag: Optional[str]
        :param kwargs: Additional attributes that are searched for (e.g. class_, id, attrs, etc.).
        :type kwargs: Any
        :return: The first matched element or None if no match is found.
        :rtype: Optional
        """
        soup = BeautifulSoup(content, "html.parser")
        return soup.find(tag, **kwargs)

    def find_elements_between_two_elements(
        self, content: str, row_designator: str, start_element: str, end_element: str
    ) -> List:
        """Finds all elements between two specified text markers within the given HTML content.

        Parses the HTML and collects all elements matching the row_designator that appear
        after the start_element and before the end_element.

        :param content: The HTML content to be parsed.
        :type content: str
        :param row_designator: Tag name used to select rows (e.g. 'tr', 'div').
        :type row_designator: str
        :param start_element: Text content that marks the start of the selection.
        :type start_element: str
        :param end_element: Text content that marks the end of the selection.
        :type end_element: str
        :return: List of elements found between the start and end markers.
        :rtype: List
        """
        soup = BeautifulSoup(content, "html.parser")
        rows = soup.find_all(row_designator)

        start_collecting = False
        result_rows = []

        for row in rows:
            if not start_collecting and row.find(string=start_element):
                start_collecting = True

            if start_collecting and row.find(string=end_element):
                break

            if start_collecting:
                result_rows.append(row)

        return result_rows

    def check_website_availabilty(self, url: str) -> bool:
        """Checks the availability of a website by sending an HTTP GET request.
        This function sends a GET request to the specified URL and checks the HTTP status code of the response.
        If the status code is 200, it indicates that the website is reachable. Any other status code indicates
        that the website may be down or returning an error.

        :param url: The URL of the website to check.
        :type url: str
        :return: True if the website is reachable (status code 200), otherwise False.
        :rtype: bool
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.logger.info(f"[Info]: Website: {url} is reachable")
                return True
            else:
                self.logger.info(
                    f"[Info]: Website: {url} returned status code {response.status_code}."
                )
                return False
        except requests.RequestException as ex:
            self.logger.error(
                f"[Error]: An error occured during checking availability of website {url}. Error code: {ex}"
            )
            return False

    def close_browser(self) -> None:
        """
        Closes the browser instance and stops the Playwright process.

        :return: None
        :rtype: None
        """
        self.browser.close()
        self.playwright.stop()
