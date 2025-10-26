#!/usr/bin/env python3

from playwright_mcp_bridge import PlaywrightMCPBridge
import sys


def test_search(url, search_term, headless=False):
    """
    test just the navigation and search functionality
    helps debug search box issues
    """
    print("=" * 60)
    print(f"testing search on: {url}")
    print(f"search term: {search_term}")
    print(f"headless: {headless}")
    print("=" * 60)
    print()
    
    browser = PlaywrightMCPBridge(headless=headless)
    
    try:
        # start browser
        browser.start()
        print("✓ browser started\n")
        
        # navigate
        print("step 1: navigating...")
        if browser.navigate(url):
            print("✓ navigation successful\n")
        else:
            print("✗ navigation failed\n")
            return False
        
        # let user inspect the page
        if not headless:
            print("inspect the page now...")
            input("press enter when ready to search...")
        
        # search
        print("\nstep 2: searching...")
        if browser.search_product(search_term):
            print("✓ search successful\n")
        else:
            print("✗ search failed\n")
            return False
        
        # let user see results
        if not headless:
            print("check the search results...")
            input("press enter to extract product info...")
        
        # extract
        print("\nstep 3: extracting product info...")
        result = browser.extract_product_info()
        
        print("\nresults:")
        print("=" * 60)
        print(f"product_name: {result.get('product_name')}")
        print(f"price: {result.get('price')}")
        print(f"product_url: {result.get('product_url')}")
        print("=" * 60)
        
        if result.get('product_name'):
            print("\n✓ test successful!")
            return True
        else:
            print("\n⚠ no product found")
            return False
        
    except Exception as e:
        print(f"\nerror: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if not headless:
            input("\npress enter to close browser...")
        browser.close()
        print("browser closed")


if __name__ == "__main__":
    # default test cases
    test_cases = {
        'digikey': ('https://www.digikey.com', 'Arduino Uno'),
        'mouser': ('https://www.mouser.com', 'Arduino Uno'),
        'adafruit': ('https://www.adafruit.com', 'Arduino'),
        'sparkfun': ('https://www.sparkfun.com', 'Arduino')
    }
    
    if len(sys.argv) < 2:
        print("usage: python test_search_only.py <site> [search_term] [--headless]")
        print("\navailable sites:")
        for site in test_cases.keys():
            print(f"  - {site}")
        print("\nexample:")
        print("  python test_search_only.py digikey 'Arduino Uno'")
        print("  python test_search_only.py digikey 'Arduino Uno' --headless")
        sys.exit(1)
    
    site = sys.argv[1].lower()
    
    if site not in test_cases:
        print(f"unknown site: {site}")
        print(f"available: {', '.join(test_cases.keys())}")
        sys.exit(1)
    
    # get search term
    if len(sys.argv) >= 3 and not sys.argv[2].startswith('--'):
        search_term = sys.argv[2]
    else:
        search_term = test_cases[site][1]
    
    # check for headless flag
    headless = '--headless' in sys.argv
    
    url = test_cases[site][0]
    
    success = test_search(url, search_term, headless)
    sys.exit(0 if success else 1)


