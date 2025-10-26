# playwright browser automation guide

## what is playwright?

playwright is a browser automation framework that lets you **actually control** real browsers (chromium, firefox, webkit). your python code can:

✅ open browser windows
✅ click buttons and fill forms
✅ navigate websites
✅ extract real data from live pages
✅ add items to real shopping carts

## setup (quick)

```bash
# install playwright
pip install playwright

# install browsers
playwright install chromium

# or use our script
./setup_playwright.sh
```

## test your setup

```bash
# interactive test
python test_browser.py

# choose visible or headless mode
# it will search for "Arduino" on adafruit.com
```

## visible vs headless mode

### visible mode (--show-browser)
**you can watch the automation happen**

```bash
python main.py example_bom.csv --show-browser
```

**what you'll see:**
- browser window opens
- navigates to each website
- searches for parts
- clicks buttons
- adds to cart
- **you can take over manually if needed**

**pros:**
- see exactly what's happening
- debug issues visually
- can intervene if needed
- educational/impressive to watch

**cons:**
- slower (waits for rendering)
- requires display/gui
- can't run on headless servers

### headless mode (--headless or default)
**runs in background, no window**

```bash
python main.py example_bom.csv --headless
```

**what happens:**
- same actions as visible mode
- browser runs in memory
- no window shown
- faster execution

**pros:**
- 30-50% faster
- works on servers without gui
- can run multiple in parallel
- less resource intensive

**cons:**
- can't see what's happening
- harder to debug
- some sites detect headless mode

## how it works

### playwright_mcp_bridge.py

this file contains the `PlaywrightMCPBridge` class that:

1. **launches browser**
```python
browser = PlaywrightMCPBridge(headless=False)  # visible
browser.start()
```

2. **navigates to website**
```python
browser.navigate("https://www.digikey.com")
```

3. **searches for parts**
```python
browser.search_product("Arduino Uno R3")
# tries multiple search box selectors
# handles different website layouts
```

4. **extracts product info**
```python
info = browser.extract_product_info()
# returns: {'product_name': '...', 'price': '...', 'product_url': '...'}
```

5. **adds to cart**
```python
result = browser.add_to_cart(product_url)
# clicks "add to cart" button
# returns cart url
```

6. **cleanup**
```python
browser.close()
```

### browser_controller.py integration

the `BrowserController` now has two modes:

**real browser mode** (default):
```python
controller = BrowserController(use_real_browser=True, headless=False)
# uses playwright to control actual browser
```

**llm simulation mode**:
```python
controller = BrowserController(use_real_browser=False)
# uses llm to generate simulated results
```

## practical examples

### example 1: watch automation on one website
```bash
python main.py example_bom.csv --show-browser --num-websites 1
```

### example 2: fast headless for production
```bash
python main.py my_bom.csv --headless --num-websites 3 --output results.csv
```

### example 3: with open source model + visible browser
```bash
python main.py example_bom.csv --use-open-source --show-browser
```

### example 4: debug mode (visible + screenshots)
edit `playwright_mcp_bridge.py` to enable screenshots:
```python
# after each action
browser.take_screenshot(f"step_{step_num}.png")
```

## supported websites

playwright can work with **any website**, but search/cart logic needs to be adapted for each site's layout.

**works best with:**
- digikey.com
- mouser.com
- adafruit.com
- sparkfun.com
- arrow.com
- newark.com
- mcmaster.com

**the bridge tries multiple selectors** to handle different layouts:
- `input[type="search"]`
- `input[name="search"]`
- `#search`
- etc.

## customizing for specific websites

edit `playwright_mcp_bridge.py` to add site-specific logic:

```python
def search_product(self, search_term: str) -> bool:
    # add custom logic for specific sites
    if 'digikey' in self.page.url:
        # digikey-specific search logic
        self.page.fill('#searchInput', search_term)
        self.page.click('#searchButton')
    elif 'mouser' in self.page.url:
        # mouser-specific search logic
        self.page.fill('[name="keyword"]', search_term)
        self.page.press('[name="keyword"]', 'Enter')
    else:
        # generic search (current implementation)
        # ... existing code ...
```

## troubleshooting

### browser doesn't open
```bash
# reinstall browsers
playwright install chromium

# check if playwright is installed
python -c "from playwright.sync_api import sync_playwright; print('ok')"
```

### search not working on specific site
- run with `--show-browser` to watch what happens
- check the site's search box selector
- add site-specific logic in `playwright_mcp_bridge.py`

### "timeout" errors
- increase timeout in playwright_mcp_bridge.py:
```python
self.page.wait_for_selector(selector, timeout=10000)  # 10 seconds
```

### captcha/bot detection
- some sites block automation
- try:
  - running in visible mode (less detection)
  - adding delays: `time.sleep(2)`
  - rotating user agents
  - using residential proxies

## performance tips

### speed up execution
1. use `--headless` (30-50% faster)
2. reduce `--num-websites` (fewer sites to search)
3. disable images/css:
```python
context = browser.new_context(
    bypass_csp=True,
    ignore_https_errors=True,
)
```

### run multiple parts in parallel
```python
# create multiple browser instances
# process parts concurrently
# (advanced - requires thread/process management)
```

## cost comparison

**with playwright:**
- free browser automation
- no api costs for browsing
- still need gemini api for website discovery
- can use free open source models for llm tasks

**total cost for 20 part bom:**
- gemini api: ~$0.10-0.50
- open source model: $0 (local)
- **total: ~$0.50 or less**

vs openai gpt-4 only (no browser): ~$10-15

## next steps

1. **test it:**
```bash
python test_browser.py
```

2. **run example:**
```bash
python main.py example_bom.csv --show-browser
```

3. **customize for your sites:**
- edit `playwright_mcp_bridge.py`
- add site-specific selectors
- test with your actual bom

4. **production:**
```bash
python main.py my_bom.csv --headless --num-websites 3
```

enjoy watching your browser automate part ordering! 🎉


