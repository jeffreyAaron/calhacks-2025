import os
import json
from typing import Dict, List, Optional
from openai import OpenAI
from playwright_mcp_bridge import PlaywrightMCPBridge


class BrowserController:
    def __init__(self, api_key: str = None, mcp_server_url: str = None, 
                 model_name: str = None, base_url: str = None, use_open_source: bool = False,
                 use_real_browser: bool = True, headless: bool = False):
        self.mcp_server_url = mcp_server_url or os.getenv('MCP_SERVER_URL', 'http://localhost:3000')
        self.use_open_source = use_open_source or os.getenv('USE_OPEN_SOURCE_MODEL', 'false').lower() == 'true'
        
        # browser automation settings
        self.use_real_browser = use_real_browser
        self.headless = headless
        
        # configure for open source or openai
        if self.use_open_source:
            # for open source models (ollama, lm studio, vllm, etc)
            self.base_url = base_url or os.getenv('OPEN_SOURCE_BASE_URL', 'http://localhost:11434/v1')
            self.model_name = model_name or os.getenv('OPEN_SOURCE_MODEL_NAME', 'llama3.1')
            # many open source apis don't require api keys
            self.api_key = api_key or os.getenv('OPEN_SOURCE_API_KEY', 'not-needed')
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            # use openai
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.model_name = model_name or os.getenv('OPENAI_MODEL_NAME', 'gpt-4')
            self.base_url = base_url
            if self.base_url:
                self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            else:
                self.client = OpenAI(api_key=self.api_key)
        
    def search_part_on_website(self, part_name: str, website_url: str) -> Dict[str, Optional[str]]:
        # use real browser automation with playwright
        if self.use_real_browser:
            return self._search_with_playwright(part_name, website_url)
        else:
            # fallback to llm-based simulation
            return self._search_with_llm(part_name, website_url)
    
    def _search_with_playwright(self, part_name: str, website_url: str) -> Dict[str, Optional[str]]:
        # use playwright to actually control a browser
        browser = PlaywrightMCPBridge(headless=self.headless)
        
        try:
            browser.start()
            
            # navigate to website
            if not browser.navigate(website_url):
                return {'product_name': None, 'price': None, 'product_url': None}
            
            # search for the part
            if not browser.search_product(part_name):
                print(f"  could not search on {website_url}")
                return {'product_name': None, 'price': None, 'product_url': None}
            
            # extract product information
            product_info = browser.extract_product_info()
            
            return product_info
            
        except Exception as e:
            print(f"  playwright error: {e}")
            return {'product_name': None, 'price': None, 'product_url': None}
        finally:
            browser.close()
    
    def _search_with_llm(self, part_name: str, website_url: str) -> Dict[str, Optional[str]]:
        # use llm to simulate browser automation (original implementation)
        prompt = f"""Using browser automation through MCP protocol:
        1. Navigate to {website_url}
        2. Search for the part: {part_name}
        3. Find the first matching product result
        4. Extract the product price and product URL
        5. Return the information in JSON format: {{"price": "XX.XX", "product_url": "https://...", "product_name": "..."}}
        
        If the part is not found, return {{"price": null, "product_url": null, "product_name": null}}
        """
        
        try:
            # use llm to interact with mcp browser automation
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a browser automation assistant using MCP protocol. Extract product information and return it in JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # parse the response to extract product info
            response_text = response.choices[0].message.content
            # try to extract json from the response
            try:
                # find json in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    product_info = json.loads(response_text[json_start:json_end])
                else:
                    product_info = {"price": None, "product_url": None, "product_name": None}
            except:
                product_info = {"price": None, "product_url": None, "product_name": None}
                
            return product_info
            
        except Exception as e:
            print(f"error searching for {part_name} on {website_url}: {e}")
            return {"price": None, "product_url": None, "product_name": None}
    
    def add_to_cart(self, product_url: str) -> Dict[str, any]:
        # add product to cart using real browser or llm
        if self.use_real_browser:
            return self._add_to_cart_with_playwright(product_url)
        else:
            return self._add_to_cart_with_llm(product_url)
    
    def _add_to_cart_with_playwright(self, product_url: str) -> Dict[str, any]:
        # use playwright to actually add to cart
        browser = PlaywrightMCPBridge(headless=self.headless)
        
        try:
            browser.start()
            result = browser.add_to_cart(product_url)
            return result
        except Exception as e:
            print(f"  playwright error adding to cart: {e}")
            return {'success': False, 'cart_url': None, 'message': str(e)}
        finally:
            browser.close()
    
    def _add_to_cart_with_llm(self, product_url: str) -> Dict[str, any]:
        # use llm to simulate adding to cart (original implementation)
        prompt = f"""Using browser automation through MCP protocol:
        1. Navigate to {product_url}
        2. Find and click the "Add to Cart" or "Add to Basket" button
        3. Wait for confirmation that the item was added
        4. Get the current cart URL
        5. Return the result in JSON format: {{"success": true/false, "cart_url": "https://...", "message": "..."}}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a browser automation assistant using MCP protocol. Perform actions and return results in JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            response_text = response.choices[0].message.content
            # try to extract json from the response
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    result = json.loads(response_text[json_start:json_end])
                else:
                    result = {"success": False, "cart_url": None, "message": "Failed to parse response"}
            except:
                result = {"success": False, "cart_url": None, "message": "Failed to parse response"}
                
            return result
            
        except Exception as e:
            print(f"error adding {product_url} to cart: {e}")
            return {"success": False, "cart_url": None, "message": str(e)}
    
    def process_part_across_websites(self, part_name: str, websites: List[str]) -> List[Dict]:
        # search for a part across multiple websites and collect results
        results = []
        for website in websites:
            print(f"  searching {part_name} on {website}")
            product_info = self.search_part_on_website(part_name, website)
            
            if product_info['product_url']:
                # if we found the product, try to add it to cart
                cart_result = self.add_to_cart(product_info['product_url'])
                product_info['cart_url'] = cart_result.get('cart_url')
                product_info['added_to_cart'] = cart_result.get('success', False)
            else:
                product_info['cart_url'] = None
                product_info['added_to_cart'] = False
            
            product_info['website'] = website
            results.append(product_info)
            
        return results

