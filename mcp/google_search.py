#!/usr/bin/env python3
"""
Search on Google using browser automation
"""

import sys
from playwright_mcp_bridge import PlaywrightMCPBridge
import time

def search_google(search_term: str):
    """Search for a term on Google"""
    browser = PlaywrightMCPBridge(headless=False)  # visible browser
    
    try:
        print(f"Starting browser automation...")
        browser.start()
        
        # Navigate to Google
        print(f"\nNavigating to Google...")
        if not browser.navigate("https://www.google.com"):
            print("Failed to navigate to Google")
            return False
        
        # Search for the term
        print(f"\nSearching for: {search_term}")
        
        # Google search box selectors
        search_selectors = [
            'textarea[name="q"]',
            'input[name="q"]',
            'textarea[title="Search"]',
            'input[title="Search"]'
        ]
        
        search_success = False
        for selector in search_selectors:
            try:
                element = browser.page.wait_for_selector(selector, timeout=3000)
                if element and element.is_visible():
                    print(f"  Found search box with: {selector}")
                    element.click()
                    time.sleep(0.5)
                    element.fill(search_term)
                    time.sleep(0.5)
                    element.press('Enter')
                    print(f"  Search submitted!")
                    search_success = True
                    break
            except Exception as e:
                print(f"  Selector {selector} failed: {e}")
                continue
        
        if not search_success:
            print("Could not find search box")
            return False
        
        # Wait for results
        print(f"\nWaiting for search results...")
        time.sleep(3)
        
        # Extract some search results
        print(f"\nSearch Results:")
        print(f"Current URL: {browser.get_current_url()}")
        
        # Try to extract result titles
        try:
            result_selectors = ['h3', '.g h3', '[data-attrid] h3']
            for selector in result_selectors:
                results = browser.page.query_selector_all(selector)
                if results:
                    print(f"\nTop results:")
                    for i, result in enumerate(results[:5], 1):
                        try:
                            title = result.inner_text().strip()
                            if title:
                                print(f"  {i}. {title}")
                        except:
                            continue
                    break
        except Exception as e:
            print(f"Could not extract results: {e}")
        
        # Keep browser open for a moment so you can see the results
        print(f"\nKeeping browser open for 10 seconds...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print(f"\nClosing browser...")
        browser.close()

if __name__ == "__main__":
    search_term = "Browser MCP"
    if len(sys.argv) > 1:
        search_term = " ".join(sys.argv[1:])
    
    print("="*50)
    print(f"Google Search Automation")
    print("="*50)
    
    search_google(search_term)

