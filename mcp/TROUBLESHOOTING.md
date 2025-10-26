# troubleshooting guide

## common issues and solutions

### 1. "could not search on [website]"

**problem:** browser opens and navigates but can't find the search box

**solution:** the website's search box selector isn't recognized

**fix options:**

#### option a: use the debug tool
```bash
python debug_selectors.py https://www.digikey.com "Arduino"
```

this will:
- open the browser
- show you all found input elements
- test searching
- show you what selectors work

then update `playwright_mcp_bridge.py` with the correct selectors.

#### option b: add site-specific selectors

edit `playwright_mcp_bridge.py` and add your site:

```python
def search_product(self, search_term: str) -> bool:
    current_url = self.page.url.lower()
    
    if 'yoursite.com' in current_url:
        return self._search_yoursite(search_term)
    # ... existing code

def _search_yoursite(self, search_term: str) -> bool:
    try:
        # use the selector you found with debug tool
        selector = 'input#your-search-box-id'
        element = self.page.wait_for_selector(selector, timeout=3000)
        element.click()
        element.fill(search_term)
        element.press('Enter')
        time.sleep(3)
        return True
    except:
        return False
```

#### option c: manual browser inspection

1. run with `--show-browser`
2. right-click the search box
3. select "inspect element"
4. note the id, name, or class
5. add that selector to playwright_mcp_bridge.py

### 2. no products found

**problem:** search works but no products extracted

**symptoms:**
```
✓ search submitted successfully
✗ no product found
```

**solution:** product container selectors need adjustment

**fix:**
```bash
# use debug tool after searching
python debug_selectors.py https://www.digikey.com "Arduino"
# after search, it will show which selectors find products
```

### 3. playwright not installed

**error:**
```
ModuleNotFoundError: No module named 'playwright'
```

**solution:**
```bash
pip install playwright
playwright install chromium
```

### 4. browser doesn't launch

**error:**
```
playwright._impl._api_types.Error: Executable doesn't exist
```

**solution:**
```bash
# install browsers
playwright install chromium

# or all browsers
playwright install
```

### 5. timeout errors

**error:**
```
TimeoutError: waiting for selector "[selector]" timeout 3000ms exceeded
```

**solutions:**

1. **increase timeout** in playwright_mcp_bridge.py:
```python
element = self.page.wait_for_selector(selector, timeout=10000)  # 10 seconds
```

2. **check if site is slow:**
```bash
# run with visible browser to watch
python main.py example_bom.csv --show-browser
```

3. **add more wait time:**
```python
time.sleep(5)  # wait longer for page to load
```

### 6. captcha/bot detection

**problem:** website shows captcha or blocks automation

**symptoms:**
- captcha page appears
- "access denied" messages
- unusual behavior

**solutions:**

1. **use visible mode** (less detection):
```bash
python main.py example_bom.csv --show-browser
```

2. **add delays** between actions:
```python
time.sleep(random.randint(2, 5))  # random delays
```

3. **use stealth mode** - update playwright_mcp_bridge.py:
```python
def start(self):
    self.playwright = sync_playwright().start()
    self.browser = self.playwright.chromium.launch(
        headless=self.headless,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox'
        ]
    )
    self.context = self.browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        extra_http_headers={
            'Accept-Language': 'en-US,en;q=0.9'
        }
    )
```

### 7. prices not extracted correctly

**problem:** finds product but price is null or wrong

**solution:** price selector needs adjustment

**fix:** edit `extract_product_info()` in playwright_mcp_bridge.py:

```python
# add more price selectors
price_selectors = [
    '.price',
    '[class*="price"]',
    '[data-price]',
    'span:has-text("$")',
    '.pricing',
    'td:has-text("$")',  # for table-based layouts
    '[class*="cost"]'
]
```

### 8. "added_to_cart" always false

**problem:** finds product but can't add to cart

**solution:** cart button selector needs adjustment

**fix:** similar to search, add site-specific cart logic:

```python
def _add_to_cart_yoursite(self, product_url: str) -> Dict:
    # navigate to product
    self.page.goto(product_url)
    
    # find YOUR site's add to cart button
    button = self.page.wait_for_selector('button#add-to-cart-button')
    button.click()
    
    return {'success': True, 'cart_url': 'https://yoursite.com/cart'}
```

### 9. gemini api errors

**error:**
```
google.generativeai.types.generation_types.BlockedPromptException
```

**solution:** gemini blocked the prompt

**fix:**
1. check your api key is valid
2. try simpler part names
3. use fallback in website_finder.py (already implemented)

### 10. ollama not responding

**error:**
```
Connection refused: http://localhost:11434
```

**solution:**
```bash
# check if ollama is running
curl http://localhost:11434/api/tags

# if not, start it
ollama serve

# in another terminal
ollama pull llama3.1
```

## debugging checklist

when something doesn't work:

- [ ] run with `--show-browser` to watch what happens
- [ ] use `debug_selectors.py` to find correct selectors
- [ ] check browser console for javascript errors
- [ ] try with a different website
- [ ] reduce `--num-websites` to 1 for testing
- [ ] add print statements in playwright_mcp_bridge.py
- [ ] enable screenshots: `browser.take_screenshot('debug.png')`

## getting help

1. **check the terminal output** - shows which step failed
2. **use debug tools:**
   - `python test_browser.py` - test basic functionality
   - `python debug_selectors.py <url> <search>` - find selectors
3. **watch the browser** - run with `--show-browser`
4. **check logs** - add more print statements

## site-specific notes

### digikey
- search: `#searchInput` or `input[data-testid="search-input"]`
- products: `tr[itemtype*="Product"]`
- usually works well with automation

### mouser
- search: `input[name="keyword"]`
- products: `.SearchResultsTableRow`
- may have regional redirects

### adafruit
- search: `input[name="q"]`
- products: `.product` or `.product-listing`
- generally automation-friendly

### sparkfun
- search: `input[name="q"]`
- products: `.product-card`
- similar to adafruit

### amazon
- **not recommended** - very aggressive bot detection
- use specialized tools for amazon scraping

## performance tips

if automation is too slow:

1. use `--headless` (30-50% faster)
2. reduce `--num-websites`
3. disable images in playwright:
```python
self.context = self.browser.new_context(
    bypass_csp=True,
    ignore_https_errors=True,
    # disable images
    extra_http_headers={'Accept': 'text/html'}
)
```

## still having issues?

1. run the debug tool and save output
2. check which step is failing
3. try with a single website first
4. verify playwright installation: `playwright --version`


