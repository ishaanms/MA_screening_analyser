"""
Website scraper for extracting company information
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time


class WebsiteScraper:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_company(self, company_name, website=None):
        """
        Scrape basic company information from website
        """
        result = {
            "name": company_name,
            "description": None,
            "mission": None,
            "founded": None,
            "employees": None,
            "headquarters": None,
            "scraped_successfully": False
        }
        
        if not website:
            return result
        
        try:
            # Ensure URL has scheme
            if not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            
            # Try to find and scrape About page
            about_content = self._scrape_about_page(website)
            if about_content:
                result.update(about_content)
                result["scraped_successfully"] = True
            
            # Fallback: scrape homepage
            if not result["description"]:
                homepage_content = self._scrape_homepage(website)
                if homepage_content:
                    result.update(homepage_content)
                    result["scraped_successfully"] = True
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _scrape_about_page(self, base_url):
        """Try to find and scrape About/Company page"""
        about_urls = [
            urljoin(base_url, '/about'),
            urljoin(base_url, '/about-us'),
            urljoin(base_url, '/company'),
            urljoin(base_url, '/about/company'),
            urljoin(base_url, '/who-we-are')
        ]
        
        for url in about_urls:
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                if response.status_code == 200:
                    return self._extract_about_info(response.text)
            except:
                continue
        
        return None
    
    def _scrape_homepage(self, url):
        """Scrape homepage for basic information"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                return self._extract_homepage_info(response.text)
        except:
            pass
        
        return None
    
    def _extract_about_info(self, html):
        """Extract information from About page"""
        soup = BeautifulSoup(html, 'html.parser')
        info = {}
        
        # Extract description (usually in first few paragraphs)
        paragraphs = soup.find_all('p')
        if paragraphs:
            # Get first substantial paragraph (>50 chars)
            for p in paragraphs[:5]:
                text = p.get_text().strip()
                if len(text) > 50:
                    info['description'] = text[:500]  # Limit to 500 chars
                    break
        
        # Try to extract mission statement (often in h2, h3, or emphasized text)
        mission_keywords = ['mission', 'vision', 'purpose', 'why we exist']
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            heading_text = heading.get_text().lower()
            if any(keyword in heading_text for keyword in mission_keywords):
                next_p = heading.find_next('p')
                if next_p:
                    info['mission'] = next_p.get_text().strip()[:300]
                    break
        
        # Extract founded year
        text = soup.get_text()
        founded_match = re.search(r'founded in (\d{4})|established (\d{4})|since (\d{4})', text, re.IGNORECASE)
        if founded_match:
            info['founded'] = founded_match.group(1) or founded_match.group(2) or founded_match.group(3)
        
        return info
    
    def _extract_homepage_info(self, html):
        """Extract basic info from homepage"""
        soup = BeautifulSoup(html, 'html.parser')
        info = {}
        
        # Try meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            info['description'] = meta_desc['content'][:500]
        
        # Try og:description
        if not info.get('description'):
            og_desc = soup.find('meta', attrs={'property': 'og:description'})
            if og_desc and og_desc.get('content'):
                info['description'] = og_desc['content'][:500]
        
        # Fallback: first heading + paragraph
        if not info.get('description'):
            h1 = soup.find('h1')
            if h1:
                first_p = soup.find('p')
                if first_p:
                    info['description'] = f"{h1.get_text()} - {first_p.get_text()}"[:500]
        
        return info


def test_scraper():
    """Test the scraper with example companies"""
    scraper = WebsiteScraper()
    
    test_companies = [
        ("Shopify", "https://www.shopify.com"),
        ("Stripe", "https://www.stripe.com"),
    ]
    
    for name, url in test_companies:
        print(f"\nScraping {name}...")
        result = scraper.scrape_company(name, url)
        print(f"Success: {result['scraped_successfully']}")
        print(f"Description: {result.get('description', 'N/A')[:100]}...")


if __name__ == "__main__":
    test_scraper()
