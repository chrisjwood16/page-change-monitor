import requests
import sys
import time
from lxml import html
from lxml import etree 

import argparse

# Initialize argument parser
parser = argparse.ArgumentParser(description='Compare HTML fetched from a URL XPath against stored HTML.')
parser.add_argument('--url', required=True, help='The URL to fetch HTML from.')
parser.add_argument('--xpath', required=True, help='The XPath to find the HTML element.')
parser.add_argument('--file_path', required=True, help='File path to store and read the HTML for comparison.')

args = parser.parse_args()
URL = args.url
XPATH = args.xpath
FILE_PATH = args.file_path



def fetch_html_by_xpath(url, xpath):
    for attempt in range(1, 4):
        try:
            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                raise requests.HTTPError(
                    f"HTTP {response.status_code}"
                )

            tree = html.fromstring(response.content)
            elements = tree.xpath(xpath)

            if not elements:
                raise ValueError(
                    "No element found for the provided XPath"
                )

            return etree.tostring(
                elements[0],
                pretty_print=True,
                method="html"
            ).decode("utf-8")

        except requests.RequestException as exc:
            print(
                f"Attempt {attempt}/3 failed for {url}: {exc}",
                flush=True
            )

            if attempt == 3:
                print(
                    f"Skipping {url} after 3 attempts",
                    flush=True
                )
                sys.exit(2)

            time.sleep(10 if attempt == 1 else 30)

def write_html_to_disk(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    # Fetch the new HTML content
    new_content = fetch_html_by_xpath(URL, XPATH)

    # Write the new HTML to disk
    write_html_to_disk(FILE_PATH, new_content)


    

