# debugging search issues

## quick test

if search isn't working, use this focused test:

```bash
# test digikey search specifically
python test_search_only.py digikey "Arduino Uno"

# this will:
# 1. open browser visibly
# 2. navigate to digikey
# 3. pause so you can inspect
# 4. try to search
# 5. show what worked/failed
```

## common issues

### issue 1: search box not found

**symptoms:**
```
looking for search box on digikey...
trying selector 1/8: #searchInput
selector #searchInput failed: Timeout
...
✗ no search box found
```

**causes:**
1. page hasn't fully loaded
2. cookie banner blocking search box
3. cloudflare challenge active
4. search box id/class changed

**solutions:**

**a) check the screenshot:**
```bash
# if browser visible, it saves digikey_debug.png
# open the image and look for the search box
# inspect element to find the actual selector
```

**b) use the test script:**
```bash
python test_search_only.py digikey
# when it pauses, right-click search box
# "inspect element" to see actual id/class
# add that selector to _search_digikey()
```

**c) increase wait time:**
edit `playwright_mcp_bridge.py`:
```python
# in navigate() method
self.page.wait_for_load_state('networkidle', timeout=15000)  # increase
time.sleep(delay + 3)  # add extra time
```

### issue 2: cloudflare blocking

**symptoms:**
```
navigating to https://www.digikey.com/
⚠️  cloudflare challenge detected - waiting for resolution...
still on cloudflare challenge
```

**solutions:**

**a) use visible mode (required):**
```bash
python main.py example_bom.csv --show-browser
```

**b) wait longer for cloudflare:**
edit `playwright_mcp_bridge.py`:
```python
if self._detect_cloudflare():
    print("cloudflare detected...")
    time.sleep(20)  # increase from 10 to 20
```

**c) manually solve if needed:**
in visible mode, you can:
- solve captcha yourself
- wait for challenge to pass
- script will continue automatically

### issue 3: cookie banner blocking

**symptoms:**
- search box exists but not clickable
- cookie consent popup in the way

**solution:** already implemented!
```python
self._dismiss_popups()  # called automatically
```

if not working, add site-specific dismissal:
```python
# in _dismiss_popups()
# add digikey-specific cookie button
'button#digikey-cookie-accept',
```

### issue 4: wrong search results

**symptoms:**
- search works
- but extracts wrong product or no product

**solution:** check product selectors

edit `extract_product_info()`:
```python
if 'digikey' in current_url:
    product_selectors = [
        'tr[itemtype*="Product"]',  # add more here
        '.your-specific-selector'
    ]
```

## debugging workflow

### step 1: test with visible browser
```bash
python test_search_only.py digikey "Arduino"
```

### step 2: watch what happens
- does page load?
- is there a popup?
- can you see the search box?
- does cloudflare challenge appear?

### step 3: inspect search box
when test pauses:
- right-click search box
- "inspect element"
- note the id, name, class
- check current selectors in code

### step 4: add selector if needed
edit `playwright_mcp_bridge.py`:
```python
def _search_digikey(self, search_term: str) -> bool:
    selectors = [
        '#searchInput',
        'your-new-selector-here',  # <-- add here
        # ...
    ]
```

### step 5: check screenshots
if visible mode, script saves:
- `digikey_debug.png` - shows page when search attempted

open and inspect to see what's visible

### step 6: check terminal output
script prints detailed debug info:
```
trying selector 1/8: #searchInput
selector #searchInput failed: Timeout
trying selector 2/8: input[data-testid="search-input"]
✓ found search box with: input[data-testid="search-input"]
```

tells you exactly which selector worked

## manual testing in browser

### test selectors in browser console:

1. open digikey in chrome
2. open developer tools (F12)
3. go to console tab
4. test selectors:

```javascript
// test if selector finds element
document.querySelector('#searchInput')

// test if it's visible
document.querySelector('#searchInput').offsetParent !== null

// list all inputs
document.querySelectorAll('input').forEach((inp, i) => {
  console.log(i, inp.id, inp.name, inp.className, inp.type)
})
```

## site-specific notes

### digikey
- uses cloudflare (must be visible mode)
- search box usually: `#searchInput`
- may have cookie banner on first visit
- products in: `tr[itemtype*="Product"]`

### mouser
- also uses cloudflare
- search box: `input[name="keyword"]`
- products in: `.SearchResultsTableRow`

### adafruit
- usually automation-friendly
- search box: `input[name="q"]`
- products: `.product`

### sparkfun
- similar to adafruit
- search box: `input[name="q"]`
- products: `.product-card`

## advanced debugging

### enable playwright debug mode

```python
# in playwright_mcp_bridge.py start()
self.browser = self.playwright.chromium.launch(
    headless=self.headless,
    slow_mo=500,  # slow down by 500ms per action
    devtools=True  # open devtools automatically
)
```

### save page html for inspection

```python
# in _search_digikey() after navigation
html = self.page.content()
with open('digikey_page.html', 'w') as f:
    f.write(html)
print("saved page html to digikey_page.html")
```

### trace playwright actions

```python
# in start()
self.context.tracing.start(screenshots=True, snapshots=True)

# in close()
self.context.tracing.stop(path="trace.zip")
```

view trace at: https://trace.playwright.dev

## getting help

when reporting issues, provide:

1. **terminal output** (all of it)
2. **screenshot** (`digikey_debug.png`)
3. **site url** you're trying to search
4. **search term** you're using
5. **visible or headless** mode
6. **what you see** in browser (if visible)

## quick fixes to try

### fix 1: just increase timeouts
```python
# everywhere you see timeout=3000
# change to timeout=10000
```

### fix 2: add more wait time
```python
# after navigation
time.sleep(10)  # wait longer

# after search
time.sleep(10)  # wait longer for results
```

### fix 3: try different site
```bash
# if digikey doesn't work, try adafruit
python test_search_only.py adafruit "Arduino"
```

### fix 4: simplify search term
```bash
# instead of "Arduino Uno R3"
# try just "Arduino"
python test_search_only.py digikey "Arduino"
```

## success checklist

✅ browser opens and shows page
✅ no cloudflare "checking browser" loop
✅ cookie banner dismissed (if any)
✅ search box found and clicked
✅ text typed into search box
✅ search submitted (press enter)
✅ results page loads
✅ product found and extracted

if ANY step fails, that's where to focus debugging!


