#!/usr/bin/env python3

from playwright.sync_api import sync_playwright
import sys


def debug_website_selectors(url, search_term):
    # debug tool to find the right selectors for a website
    print("=" * 60)
    print(f"debugging selectors for: {url}")
    print("=" * 60)
    print()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # navigate
            print(f"navigating to {url}...")
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            print("✓ loaded")
            print()
            
            # wait for user to see the page
            input("press enter when page is loaded...")
            
            # find search boxes
            print("\nsearching for search input boxes...")
            search_selectors = [
                'input[type="search"]',
                'input[name="search"]',
                'input[name="q"]',
                'input[name="keywords"]',
                'input[id*="search" i]',
                'input[placeholder*="Search" i]',
                '#searchInput',
                '#search-input',
                '.search-input',
                '[data-testid="search-input"]'
            ]
            
            found_inputs = []
            for selector in search_selectors:
                try:
                    elements = page.query_selector_all(selector)
                    for elem in elements:
                        if elem.is_visible():
                            attrs = {
                                'tag': elem.evaluate('el => el.tagName'),
                                'id': elem.get_attribute('id'),
                                'name': elem.get_attribute('name'),
                                'class': elem.get_attribute('class'),
                                'placeholder': elem.get_attribute('placeholder'),
                                'type': elem.get_attribute('type')
                            }
                            found_inputs.append({
                                'selector': selector,
                                'attributes': attrs
                            })
                            print(f"✓ found: {selector}")
                            print(f"  attributes: {attrs}")
                except:
                    pass
            
            if not found_inputs:
                print("✗ no search inputs found!")
                print("\ntrying to list ALL input elements:")
                all_inputs = page.query_selector_all('input')
                for i, inp in enumerate(all_inputs[:10]):
                    try:
                        if inp.is_visible():
                            print(f"\ninput {i}:")
                            print(f"  id: {inp.get_attribute('id')}")
                            print(f"  name: {inp.get_attribute('name')}")
                            print(f"  class: {inp.get_attribute('class')}")
                            print(f"  type: {inp.get_attribute('type')}")
                            print(f"  placeholder: {inp.get_attribute('placeholder')}")
                    except:
                        pass
            
            # try to search if we found an input
            if found_inputs and search_term:
                print(f"\ntrying to search for: {search_term}")
                best_input = found_inputs[0]['selector']
                try:
                    element = page.wait_for_selector(best_input, timeout=2000)
                    element.click()
                    element.fill(search_term)
                    element.press('Enter')
                    print(f"✓ search submitted with: {best_input}")
                    
                    # wait for results
                    input("\npress enter to check for product results...")
                    
                    # find product containers
                    print("\nsearching for product result containers...")
                    product_selectors = [
                        '.product',
                        '.item',
                        '[data-product]',
                        '.search-result-item',
                        '.product-card',
                        'tr[class*="result"]',
                        'tr[itemtype*="Product"]',
                        'table tbody tr'
                    ]
                    
                    for selector in product_selectors:
                        try:
                            products = page.query_selector_all(selector)
                            if products and len(products) > 0:
                                visible_count = sum(1 for p in products if p.is_visible())
                                if visible_count > 0:
                                    print(f"✓ found {visible_count} products with: {selector}")
                        except:
                            pass
                    
                except Exception as e:
                    print(f"✗ search failed: {e}")
            
            print("\nbrowser will stay open. close it when done.")
            input("press enter to close browser...")
            
        except Exception as e:
            print(f"error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python debug_selectors.py <url> [search_term]")
        print("\nexamples:")
        print("  python debug_selectors.py https://www.digikey.com 'Arduino'")
        print("  python debug_selectors.py https://www.mouser.com 'resistor'")
        sys.exit(1)
    
    url = sys.argv[1]
    search_term = sys.argv[2] if len(sys.argv) > 2 else None
    
    debug_website_selectors(url, search_term)


