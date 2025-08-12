# agent_tools.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from langchain_community.tools.tavily_search import TavilySearchResults

# --- The Master List of Known Domains ---
KNOWN_TRACKER_DOMAINS = [
    "google-analytics.com", "googletagmanager.com", "doubleclick.net",
    "facebook.net", "fbcdn.net", "connect.facebook.net",
    "krxd.net", "scorecardresearch.com", "criteo.com", "amazon-adsystem.com",
    "adobedtm.com", "track.adform.net"
]

# --- Tool 1: The Field Agent's Scanner ---
def scan_website(url: str) -> dict:
    """A comprehensive scraper that gathers scripts and third-party cookies for the Field Agent."""
    print(f"--- FIELD AGENT: Deploying Selenium scanner to {url}...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        scripts = {urlparse(tag['src']).netloc for tag in soup.find_all(['script', 'iframe'], src=True) if urlparse(tag['src']).netloc}
        
        page_domain = urlparse(url).netloc
        cookies = {cookie.get('domain', '').lstrip('.') for cookie in driver.get_cookies() if page_domain not in cookie.get('domain', '').lstrip('.')}

        recon_data = {"scripts": list(scripts), "cookies": list(cookies)}
        print(f"--- FIELD AGENT: Scan complete. Data returned: {recon_data}")
        return recon_data

    except Exception as e:
        print(f"Error in Field Agent's scanner tool: {e}")
        return {"scripts": [], "cookies": []}
    finally:
        if driver:
            driver.quit()

# --- Tool 2: The OSINT Analyst's Web Searcher ---
web_search_tool = TavilySearchResults(k=1, description="A tool to search the live internet for information on domains, companies, and technologies.")