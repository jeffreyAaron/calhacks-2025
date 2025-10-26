"""
Simple example of using Claude to automate browser for BOM part search
"""
import os
from claude_browser_automation import ClaudeBrowserAutomation


def main():
    # Make sure ANTHROPIC_API_KEY is set
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set it, run:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        return
    
    print("=" * 70)
    print("🤖 Claude Browser Automation - Simple Example")
    print("=" * 70)
    print()
    
    # Create automation instance
    # headless=False means browser window will be visible (recommended)
    automation = ClaudeBrowserAutomation(headless=False)
    
    # Choose a website to search on
    # Options: 
    # - https://www.adafruit.com (good for maker electronics)
    # - https://www.sparkfun.com (good for hobbyist electronics)
    # - https://www.digikey.com (huge selection, but has Cloudflare)
    # - https://www.mouser.com (huge selection, but has Cloudflare)
    
    website = "https://www.adafruit.com"
    
    print(f"🌐 Will search on: {website}")
    print(f"📄 Using BOM file: example_bom.csv")
    print()
    
    # Process all parts in the BOM
    results = automation.process_bom_parts(
        csv_file="example_bom.csv",
        website_url=website
    )
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 Results Summary:")
    print("=" * 70)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['bom_part_name']}")
        if result['product_name']:
            print(f"   ✅ Found: {result['product_name']}")
            print(f"   💰 Price: {result['price']}")
            print(f"   🔗 URL: {result['product_url']}")
            if result.get('added_to_cart'):
                print(f"   🛒 Added to cart: YES")
            else:
                print(f"   🛒 Added to cart: NO")
        else:
            print(f"   ❌ Not found")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()

