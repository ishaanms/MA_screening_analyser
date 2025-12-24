"""
Data collection orchestrator - gathers information from multiple sources
"""

from scrapers.website_scraper import WebsiteScraper
import time


class DataCollector:
    def __init__(self, mode='fast'):
        """
        Initialize data collector
        mode: 'fast' or 'deep'
        """
        self.mode = mode
        self.website_scraper = WebsiteScraper()
    
    def collect_company_data(self, company_name, website=None, industry=None):
        """
        Collect comprehensive company data
        
        Returns:
            dict: Collected company information
        """
        data = {
            "name": company_name,
            "industry": industry,
            "website": website,
            "data_sources": []
        }
        
        # Always scrape website in both modes
        if website:
            try:
                scraped = self.website_scraper.scrape_company(company_name, website)
                if scraped.get('scraped_successfully'):
                    data.update({
                        "description": scraped.get('description'),
                        "mission": scraped.get('mission'),
                        "founded": scraped.get('founded'),
                        "employees": scraped.get('employees'),
                        "headquarters": scraped.get('headquarters')
                    })
                    data["data_sources"].append("website")
            except Exception as e:
                data["website_error"] = str(e)
        
        # Deep mode: additional data sources
        if self.mode == 'deep':
            # In Phase 3, we'll add:
            # - LinkedIn scraping
            # - News aggregation
            # - Crunchbase data
            pass
        
        return data
    
    def collect_deal_data(self, acquirer_name, acquirer_website, acquirer_industry,
                         target_name, target_website, target_industry):
        """
        Collect data for both acquirer and target
        
        Returns:
            dict: Combined data for the deal
        """
        print(f"🔍 Collecting {self.mode} mode data...")
        
        # Collect acquirer data
        print(f"  → Scraping acquirer: {acquirer_name}")
        acquirer_data = self.collect_company_data(
            acquirer_name, 
            acquirer_website, 
            acquirer_industry
        )
        
        # Small delay to be respectful to servers
        time.sleep(1)
        
        # Collect target data
        print(f"  → Scraping target: {target_name}")
        target_data = self.collect_company_data(
            target_name,
            target_website,
            target_industry
        )
        
        return {
            "acquirer": acquirer_data,
            "target": target_data,
            "collection_mode": self.mode,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }


def test_collector():
    """Test data collection"""
    collector = DataCollector(mode='fast')
    
    result = collector.collect_deal_data(
        acquirer_name="Shopify",
        acquirer_website="https://www.shopify.com",
        acquirer_industry="E-commerce/Retail",
        target_name="Deliverr",
        target_website="https://www.deliverr.com",
        target_industry="E-commerce/Retail"
    )
    
    print("\n=== Collection Results ===")
    print(f"Acquirer sources: {result['acquirer'].get('data_sources')}")
    print(f"Target sources: {result['target'].get('data_sources')}")
    print(f"Acquirer desc: {result['acquirer'].get('description', 'N/A')[:100]}...")
    print(f"Target desc: {result['target'].get('description', 'N/A')[:100]}...")


if __name__ == "__main__":
    test_collector()
