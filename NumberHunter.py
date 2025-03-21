import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_phone_numbers(html_content):
    # Regular expression to find phone numbers in various formats
    phone_regex = re.compile(r'\+[\d\s\-()]+')
    phone_numbers = phone_regex.findall(html_content)
    return phone_numbers

def crawl_website(url, visited_urls=set()):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            phone_numbers = extract_phone_numbers(html_content)
            if phone_numbers:
                print(f"Telefonnummern auf {url}: {phone_numbers}")
            
            visited_urls.add(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if next_url not in visited_urls:
                    crawl_website(next_url, visited_urls)
        else:
            print(f"Fehler: Statuscode {response.status_code}")
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Seite {url}: {e}")

if __name__ == "__main__":
    start_url = input("Geben Sie die Start-URL ein: ")
    crawl_website(start_url)