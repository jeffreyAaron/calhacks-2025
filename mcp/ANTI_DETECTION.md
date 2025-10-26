# anti-detection guide for browser automation

## the problem

modern e-commerce sites (especially digikey, mouser) use cloudflare and other bot detection:
- detects headless browsers instantly
- challenges suspicious behavior with captcha
- blocks automated requests

## implemented anti-detection measures

### 1. realistic browser fingerprint

```python
# real chrome user agent
user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# realistic headers
extra_http_headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'DNT': '1',
    # ... more headers
}
```

### 2. hide automation signals

```javascript
// override navigator.webdriver
Object.defineProperty(navigator, 'webdriver', {
    get: () => false
});

// fake plugins, languages, chrome object
```

### 3. human-like delays

**after navigation:**
- random 3-5 second wait (humans don't interact instantly)

**before typing:**
- 0.5-1.5 second delay (humans pause before typing)

**typing speed:**
- 100-250ms between keystrokes (realistic typing)

**before submitting search:**
- 0.5-1 second pause (humans review before pressing enter)

### 4. cloudflare detection

automatically detects and waits for cloudflare challenges:
```python
if 'checking your browser' in page_content:
    print("cloudflare detected, waiting...")
    time.sleep(10)
```

## best practices

### ✅ DO

1. **use visible browser mode** (--show-browser)
   ```bash
   python main.py example_bom.csv --show-browser
   ```
   cloudflare detects headless chromium instantly

2. **add delays between different parts**
   ```bash
   # don't search 20 parts in rapid succession
   # current implementation already has delays
   ```

3. **use real IP address**
   - don't use vpn/proxy unless necessary
   - residential proxies are better than datacenter

4. **limit concurrent requests**
   - search one part at a time (current default)
   - don't open multiple browser instances

5. **vary behavior slightly**
   - random delays (implemented)
   - vary typing speed (implemented)

### ❌ DON'T

1. **don't use headless mode for protected sites**
   ```bash
   # this will likely get blocked:
   python main.py example_bom.csv --headless
   ```

2. **don't spam requests**
   - avoid searching same part repeatedly
   - don't run script constantly

3. **don't use obvious datacenter IPs**
   - aws/gcp/azure IPs are flagged
   - use residential connection if possible

4. **don't disable javascript**
   - cloudflare requires js for challenges

## recommended settings

### for digikey/mouser (cloudflare protected)

```bash
# best: visible browser, one website at a time
python main.py example_bom.csv --show-browser --num-websites 1

# if you must automate many parts:
# - use visible mode
# - add longer delays between parts (edit main.py)
# - consider running at night (lower traffic = less scrutiny)
```

### for smaller sites (adafruit, sparkfun)

```bash
# headless usually works fine
python main.py example_bom.csv --headless
```

## handling captchas

### if you get a captcha:

1. **visible mode** - solve it manually
   ```bash
   python main.py example_bom.csv --show-browser
   # browser stays open, you can solve captcha
   ```

2. **add longer delays**
   edit `playwright_mcp_bridge.py`:
   ```python
   self.min_delay = 5.0  # increase from 2.0
   self.max_delay = 10.0  # increase from 5.0
   ```

3. **reduce frequency**
   - search fewer websites
   - process fewer parts at once
   - add delays between runs

4. **use captcha solving service** (advanced)
   - 2captcha.com
   - anti-captcha.com
   - integrate with playwright

## cloudflare challenge page

if you see "checking your browser":

```bash
# the script will automatically:
1. detect cloudflare challenge
2. wait 10 seconds for it to resolve
3. continue if successful
```

**in visible mode:**
- you'll see the cloudflare spinner
- wait for it to complete
- script continues automatically

**in headless mode:**
- likely will never pass (cloudflare detects headless)
- use --show-browser instead

## proxy setup (advanced)

if you need to use proxies:

```python
# edit playwright_mcp_bridge.py start() method
self.context = self.browser.new_context(
    proxy={
        'server': 'http://proxy-server:8080',
        'username': 'user',
        'password': 'pass'
    },
    # ... other settings
)
```

**proxy recommendations:**
- residential proxies (best)
- rotating proxies
- avoid: free proxies, datacenter IPs

## monitoring for blocks

watch for these signs:

1. **captcha pages**
   - "verify you are human"
   - recaptcha challenges

2. **access denied**
   - 403 forbidden
   - cloudflare block page

3. **empty results**
   - searches return no products
   - different from legitimate "not found"

4. **slow performance**
   - pages taking very long to load
   - might indicate rate limiting

## rate limiting strategy

```python
# add to main.py between parts
import time
import random

# after processing each part:
delay = random.uniform(10, 20)  # 10-20 seconds between parts
print(f"waiting {delay:.0f}s before next part (rate limiting)...")
time.sleep(delay)
```

## success metrics

**good signs:**
- searches complete successfully
- prices extracted correctly
- no captcha challenges
- no cloudflare blocks

**bad signs:**
- frequent captchas
- "checking your browser" loops
- 403/blocked pages
- empty search results

## legal considerations

**important:** respect website terms of service

- check robots.txt
- review terms of use
- don't overload servers
- consider official apis:
  - digikey has official api
  - mouser has official api
  - may be better than scraping

## alternative: official apis

instead of browser automation, use official apis:

**digikey api:**
- https://developer.digikey.com/
- requires registration
- no scraping issues

**mouser api:**
- https://www.mouser.com/api-hub/
- official part search
- rate limits but stable

**pros:**
- no bot detection
- stable and reliable
- faster
- terms-compliant

**cons:**
- requires api keys
- may have costs
- limited free tier

## summary

✅ **use visible mode for cloudflare sites**
✅ **add human-like delays (implemented)**
✅ **limit request frequency**
✅ **use real user agent (implemented)**
✅ **monitor for blocks**

❌ **avoid headless for protected sites**
❌ **don't spam requests**
❌ **don't use obvious automation patterns**

**recommended command:**
```bash
python main.py example_bom.csv --show-browser --num-websites 2
```

this balances automation with stealthiness.


