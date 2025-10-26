"""
Claude-powered browser automation using MCP tools
This script uses Claude to intelligently control the browser and search for BOM parts
"""
import os
import json
import time
from typing import Dict, List, Optional
from anthropic import Anthropic
from bom_parser import BOMParser
from playwright_mcp_bridge import PlaywrightMCPBridge


class ClaudeBrowserAutomation:
    def __init__(self, api_key: str = None, headless: bool = False):
        """
        Initialize Claude browser automation
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            headless: Whether to run browser in headless mode
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Set it as environment variable or pass as argument.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.headless = headless
        self.browser = None
        
        # Claude model to use
        self.model = "claude-3-haiku-20240307"  # Claude 3 Haiku
        
    def start_browser(self):
        """Start the browser session"""
        print("🌐 Starting browser...")
        self.browser = PlaywrightMCPBridge(headless=self.headless)
        self.browser.start()
        print("✅ Browser started successfully\n")
        
    def close_browser(self):
        """Close the browser session"""
        if self.browser:
            print("\n🔚 Closing browser...")
            self.browser.close()
            self.browser = None
    
    def get_browser_state(self) -> str:
        """Get current browser state for Claude"""
        if not self.browser or not self.browser.page:
            return "Browser not started"
        
        try:
            current_url = self.browser.get_current_url()
            page_title = self.browser.page.title()
            return f"Current URL: {current_url}\nPage Title: {page_title}"
        except:
            return "Browser state unknown"
    
    def search_part_with_claude(self, part_name: str, description: str, website_url: str) -> Dict[str, Optional[str]]:
        """
        Use Claude to intelligently search for a part and extract information
        
        Args:
            part_name: Name of the part to search for
            description: Description of the part
            website_url: Website to search on
            
        Returns:
            Dictionary with product_name, price, and product_url
        """
        print(f"🔍 Searching for '{part_name}' on {website_url}")
        
        # Navigate to website
        if not self.browser.navigate(website_url):
            print("❌ Failed to navigate to website")
            return {'product_name': None, 'price': None, 'product_url': None}
        
        # Ask Claude to analyze the page and perform the search
        browser_state = self.get_browser_state()
        
        prompt = f"""You are controlling a web browser to search for electronic components.

Current browser state:
{browser_state}

Task: Search for the following part:
- Part Name: {part_name}
- Description: {description}

Instructions:
1. I have already navigated to {website_url}
2. You need to guide me on how to search for this part
3. Tell me what search terms to use and what to look for
4. Be specific about what elements to click or interact with

Based on the website, what should I search for to find this part? Give me the exact search term."""

        try:
            # Get Claude's guidance on search strategy
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            
            search_term = response.content[0].text.strip()
            print(f"🤖 Claude suggests searching for: {search_term}")
            
            # Perform the search
            if not self.browser.search_product(part_name):
                print("❌ Search failed")
                return {'product_name': None, 'price': None, 'product_url': None}
            
            # Extract product information
            product_info = self.browser.extract_product_info()
            
            if product_info['product_name']:
                print(f"✅ Found: {product_info['product_name']} - {product_info['price']}")
            else:
                print("❌ No product found")
            
            return product_info
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return {'product_name': None, 'price': None, 'product_url': None}
    
    def add_to_cart_with_claude(self, product_url: str, part_name: str) -> Dict[str, any]:
        """
        Use Claude to guide adding product to cart
        
        Args:
            product_url: URL of the product page
            part_name: Name of the part (for context)
            
        Returns:
            Dictionary with success status, cart_url, and message
        """
        print(f"🛒 Adding {part_name} to cart...")
        
        try:
            # Navigate to product page
            if product_url:
                print(f"  → Navigating to product page...")
                self.browser.page.goto(product_url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(2)
            
            # Ask Claude for guidance on adding to cart
            browser_state = self.get_browser_state()
            
            prompt = f"""You are controlling a web browser to add an item to cart.

Current browser state:
{browser_state}

Task: Add the product "{part_name}" to the shopping cart.

The product page should be loaded. What are common button texts or attributes I should look for to add this item to cart?
List 3-5 possible button texts or selectors."""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            
            guidance = response.content[0].text.strip()
            print(f"🤖 Claude's guidance: {guidance[:100]}...")
            
            # Attempt to add to cart using the browser automation
            result = self.browser.add_to_cart()
            
            if result['success']:
                print(f"✅ Added to cart successfully!")
            else:
                print(f"❌ Failed to add to cart: {result['message']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error adding to cart: {e}")
            return {
                'success': False,
                'cart_url': None,
                'message': str(e)
            }
    
    def process_bom_parts(self, csv_file: str, website_url: str) -> List[Dict]:
        """
        Process all parts from BOM CSV file
        
        Args:
            csv_file: Path to the BOM CSV file
            website_url: Website to search on (e.g., https://www.digikey.com)
            
        Returns:
            List of results for each part
        """
        print("=" * 60)
        print("🤖 CLAUDE BROWSER AUTOMATION - BOM PARTS SEARCH")
        print("=" * 60)
        print(f"📄 BOM File: {csv_file}")
        print(f"🌐 Website: {website_url}")
        print("=" * 60)
        print()
        
        # Parse BOM
        parser = BOMParser(csv_file)
        parts = parser.get_parts()
        
        # Filter out empty rows
        parts = [p for p in parts if p.get('part_name', '').strip()]
        
        print(f"📦 Found {len(parts)} parts in BOM\n")
        
        # Start browser
        self.start_browser()
        
        results = []
        
        try:
            for i, part in enumerate(parts, 1):
                print(f"\n{'='*60}")
                print(f"Part {i}/{len(parts)}: {part['part_name']}")
                print(f"{'='*60}")
                
                part_name = part.get('part_name', '')
                description = part.get('description', '')
                quantity = part.get('quantity', '')
                
                # Search for the part
                product_info = self.search_part_with_claude(
                    part_name=part_name,
                    description=description,
                    website_url=website_url
                )
                
                # Add additional BOM information
                product_info['bom_part_name'] = part_name
                product_info['bom_description'] = description
                product_info['bom_quantity'] = quantity
                product_info['website'] = website_url
                
                # Try to add to cart if product was found
                if product_info['product_url']:
                    cart_result = self.add_to_cart_with_claude(
                        product_url=product_info['product_url'],
                        part_name=part_name
                    )
                    product_info['cart_url'] = cart_result.get('cart_url')
                    product_info['added_to_cart'] = cart_result.get('success', False)
                else:
                    product_info['cart_url'] = None
                    product_info['added_to_cart'] = False
                
                results.append(product_info)
                
                # Small delay between parts
                time.sleep(1)
                
        finally:
            # Always close browser
            self.close_browser()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        
        found_count = sum(1 for r in results if r['product_name'])
        cart_count = sum(1 for r in results if r.get('added_to_cart'))
        
        print(f"✅ Parts found: {found_count}/{len(results)}")
        print(f"🛒 Added to cart: {cart_count}/{len(results)}")
        print("=" * 60)
        
        return results


def main():
    """Main function to run the automation"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Claude-powered browser automation for BOM parts search'
    )
    parser.add_argument(
        'csv_file',
        type=str,
        help='Path to the BOM CSV file'
    )
    parser.add_argument(
        '--website',
        type=str,
        default='https://www.digikey.com',
        help='Website to search on (default: digikey.com)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (not recommended for Cloudflare-protected sites)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='Anthropic API key (defaults to ANTHROPIC_API_KEY env var)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output JSON file to save results'
    )
    
    args = parser.parse_args()
    
    # Create automation instance
    automation = ClaudeBrowserAutomation(
        api_key=args.api_key,
        headless=args.headless
    )
    
    # Process BOM parts
    results = automation.process_bom_parts(
        csv_file=args.csv_file,
        website_url=args.website
    )
    
    # Save results to JSON if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")
    
    # Also print results as JSON
    print("\n" + "=" * 60)
    print("📋 DETAILED RESULTS (JSON)")
    print("=" * 60)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

