#!/usr/bin/env python3

from playwright_mcp_bridge import PlaywrightMCPBridge
import sys


def test_browser_automation():
    print("=" * 60)
    print("testing playwright browser automation")
    print("=" * 60)
    print()
    
    # ask user for mode
    print("choose mode:")
    print("1. visible browser (you can watch)")
    print("2. headless browser (invisible, faster)")
    choice = input("enter 1 or 2: ").strip()
    
    headless = choice == "2"
    
    print()
    print(f"starting browser in {'headless' if headless else 'visible'} mode...")
    print()
    
    # create browser instance
    browser = PlaywrightMCPBridge(headless=headless)
    
    try:
        # start browser
        browser.start()
        print("✓ browser started")
        
        # test with adafruit (usually has good search)
        test_url = "https://www.adafruit.com"
        test_part = "Arduino"
        
        print(f"\ntest: searching for '{test_part}' on {test_url}")
        print("-" * 60)
        
        # navigate
        if browser.navigate(test_url):
            print("✓ navigation successful")
        else:
            print("✗ navigation failed")
            return
        
        # search
        if browser.search_product(test_part):
            print("✓ search successful")
        else:
            print("✗ search failed")
            browser.close()
            return
        
        # extract product info
        product_info = browser.extract_product_info()
        
        print("\nresults:")
        print("-" * 60)
        print(f"product name: {product_info.get('product_name', 'not found')}")
        print(f"price: {product_info.get('price', 'not found')}")
        print(f"url: {product_info.get('product_url', 'not found')}")
        
        if product_info.get('product_name'):
            print("\n✓ playwright browser automation is working!")
            
            # ask if want to test add to cart
            if product_info.get('product_url'):
                print("\nwant to test adding to cart? (y/n): ", end="")
                try:
                    response = input().strip().lower()
                    if response == 'y':
                        print("\ntesting add to cart...")
                        cart_result = browser.add_to_cart(product_info['product_url'])
                        if cart_result.get('success'):
                            print(f"✓ add to cart successful!")
                            print(f"cart url: {cart_result.get('cart_url', 'not found')}")
                        else:
                            print(f"⚠ add to cart failed: {cart_result.get('message')}")
                except:
                    pass
        else:
            print("\n⚠ no product found - this might be a website-specific issue")
            print("  try different websites or adjust selectors")
        
        if not headless:
            print("\nbrowser will close in 5 seconds...")
            import time
            time.sleep(5)
        
    except Exception as e:
        print(f"\n✗ error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        browser.close()
        print("\n✓ browser closed")
    
    print()
    print("=" * 60)
    print("test complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_browser_automation()
    except KeyboardInterrupt:
        print("\n\ntest interrupted by user")
        sys.exit(0)


