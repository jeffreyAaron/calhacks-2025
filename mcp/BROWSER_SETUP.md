# browser automation setup

## current status

the current `browser_controller.py` sends instructions to an llm, but **does not actually control a browser yet**. you need to add one of these solutions:

## option 1: playwright with mcp (recommended)

playwright can run in **headed** (visible) or **headless** (invisible) mode.

### install playwright
```bash
pip install playwright mcp
playwright install chromium
```

### create playwright mcp bridge
```python
# playwright_mcp_bridge.py
from playwright.sync_api import sync_playwright
import json

class PlaywrightMCPBridge:
    def __init__(self, headless=False):
        # headless=False means browser window is VISIBLE
        # headless=True means browser runs in background (faster)
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None
        
    def start(self):
        # start playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless  # <-- controls visibility
        )
        self.page = self.browser.new_page()
        
    def navigate(self, url):
        # navigate to url
        self.page.goto(url)
        
    def search_product(self, search_term):
        # find search box and search
        try:
            # try common search selectors
            search_selectors = [
                'input[type="search"]',
                'input[name="search"]',
                '#search',
                '[placeholder*="Search"]'
            ]
            
            for selector in search_selectors:
                if self.page.query_selector(selector):
                    self.page.fill(selector, search_term)
                    self.page.press(selector, 'Enter')
                    self.page.wait_for_load_state('networkidle')
                    return True
            return False
        except Exception as e:
            print(f"error searching: {e}")
            return False
    
    def extract_product_info(self):
        # extract product info from page
        try:
            # wait for results
            self.page.wait_for_selector('.product, .item, [data-product]', timeout=5000)
            
            # get first product
            product = self.page.query_selector('.product, .item, [data-product]')
            if product:
                name = product.query_selector('h2, h3, .title, .name')
                price = product.query_selector('.price, [class*="price"]')
                link = product.query_selector('a')
                
                return {
                    'product_name': name.inner_text() if name else None,
                    'price': price.inner_text() if price else None,
                    'product_url': link.get_attribute('href') if link else None
                }
        except:
            pass
        
        return {'product_name': None, 'price': None, 'product_url': None}
    
    def add_to_cart(self):
        # find and click add to cart button
        try:
            cart_buttons = [
                'button:has-text("Add to Cart")',
                'button:has-text("Add to Basket")',
                '[data-action="add-to-cart"]',
                '#add-to-cart'
            ]
            
            for selector in cart_buttons:
                if self.page.query_selector(selector):
                    self.page.click(selector)
                    self.page.wait_for_timeout(1000)
                    return True
            return False
        except:
            return False
    
    def close(self):
        # close browser
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
```

### update browser_controller.py
```python
# add to browser_controller.py
from playwright_mcp_bridge import PlaywrightMCPBridge

class BrowserController:
    def __init__(self, ..., headless=False):
        # ... existing code ...
        
        # add playwright bridge
        self.use_real_browser = True  # enable real browser
        self.headless = headless
        self.browser = None
        
    def search_part_on_website(self, part_name: str, website_url: str):
        if self.use_real_browser:
            # use real browser automation
            browser = PlaywrightMCPBridge(headless=self.headless)
            browser.start()
            
            try:
                browser.navigate(website_url)
                browser.search_product(part_name)
                product_info = browser.extract_product_info()
                return product_info
            finally:
                browser.close()
        else:
            # use llm-based approach (current implementation)
            # ... existing code ...
```

## option 2: selenium (more common, easier)

selenium is simpler to set up and also supports headed/headless modes.

### install selenium
```bash
pip install selenium webdriver-manager
```

### create selenium controller
```python
# selenium_controller.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class SeleniumController:
    def __init__(self, headless=False):
        # set up chrome options
        options = Options()
        if headless:
            options.add_argument('--headless')  # invisible
        else:
            # browser window will be VISIBLE
            pass
        
        # create driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
    def search_part(self, part_name, website_url):
        # navigate to website
        self.driver.get(website_url)
        time.sleep(2)
        
        # find search box
        try:
            search_box = self.driver.find_element(By.CSS_SELECTOR, 
                'input[type="search"], input[name="search"], #search')
            search_box.send_keys(part_name)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            
            # get first product
            product = self.driver.find_element(By.CSS_SELECTOR, 
                '.product, .item')
            name = product.find_element(By.CSS_SELECTOR, 'h2, h3').text
            price = product.find_element(By.CSS_SELECTOR, '.price').text
            url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
            
            return {
                'product_name': name,
                'price': price,
                'product_url': url
            }
        except Exception as e:
            print(f"error: {e}")
            return {'product_name': None, 'price': None, 'product_url': None}
    
    def close(self):
        self.driver.quit()
```

## option 3: hybrid approach (llm + browser)

use the llm to generate selectors and logic, then execute with real browser:

```python
class HybridController:
    def __init__(self, llm_controller, browser_bridge, headless=False):
        self.llm = llm_controller
        self.browser = browser_bridge(headless=headless)
        
    def search_part(self, part_name, website_url):
        # 1. ask llm for strategy
        strategy = self.llm.get_search_strategy(website_url)
        
        # 2. execute with real browser
        self.browser.start()
        self.browser.execute_strategy(strategy, part_name)
        result = self.browser.get_results()
        self.browser.close()
        
        return result
```

## controlling visibility

### visible browser (headed mode)
```python
# you can WATCH the automation happen
controller = BrowserController(headless=False)  # browser visible
```

**pros:**
- see what's happening
- easier to debug
- can manually intervene

**cons:**
- slower
- requires display/gui
- can't run on headless servers

### invisible browser (headless mode)
```python
# runs in background, no window
controller = BrowserController(headless=True)  # browser invisible
```

**pros:**
- faster (30-50% speed improvement)
- works on servers without gui
- can run multiple in parallel

**cons:**
- can't see what's happening
- harder to debug
- some websites detect headless mode

## recommended approach

1. **development**: use `headless=False` to watch and debug
2. **production**: use `headless=True` for speed

## quick implementation

want me to implement one of these? i recommend:
- **selenium** for simplicity and reliability
- **playwright** for modern features and speed

let me know which you prefer and i'll integrate it!

## example usage after implementation

```bash
# watch browser automation (visible window)
python main.py example_bom.csv --use-open-source --show-browser

# run in background (faster)
python main.py example_bom.csv --use-open-source --headless
```


