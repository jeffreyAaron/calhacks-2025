from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import random
from typing import Dict, Optional


class PlaywrightMCPBridge:
    def __init__(self, headless=False):
        # headless=False means browser window is VISIBLE (recommended for cloudflare sites)
        # headless=True means browser runs in background (faster but detected by cloudflare)
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
        # human-like behavior settings
        self.min_delay = 2.0
        self.max_delay = 5.0
        self.typing_delay_min = 100
        self.typing_delay_max = 250
        
    def start(self):
        # start playwright and launch browser with stealth settings
        if self.headless:
            print(f"  ⚠️  warning: headless mode may be detected by cloudflare/digikey")
            print(f"  consider using --show-browser for better success rate")
        
        print(f"  launching browser (headless={self.headless})...")
        self.playwright = sync_playwright().start()
        
        # launch with anti-detection args
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu'
            ]
        )
        
        # create context with realistic browser fingerprint
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/Los_Angeles',
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
        )
        
        self.page = self.context.new_page()
        
        # add stealth javascript to hide automation
        self.page.add_init_script("""
            // overwrite the navigator.webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
            
            // overwrite the navigator.plugins property
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // overwrite the navigator.languages property
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // chrome property
            window.chrome = {
                runtime: {}
            };
            
            // permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
        
    def navigate(self, url: str) -> bool:
        # navigate to url with human-like behavior
        try:
            print(f"  navigating to {url}")
            self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            
            # wait for page to be more fully loaded
            try:
                self.page.wait_for_load_state('networkidle', timeout=10000)
            except:
                pass  # continue anyway
            
            # human-like delay after navigation (3-5 seconds)
            delay = random.uniform(self.min_delay, self.max_delay)
            print(f"  waiting {delay:.1f}s (mimicking human behavior)...")
            time.sleep(delay)
            
            # check if we hit cloudflare challenge
            if self._detect_cloudflare():
                print(f"  ⚠️  cloudflare challenge detected - waiting for resolution...")
                time.sleep(10)  # give cloudflare time to resolve
            
            # handle cookie banners and popups
            self._dismiss_popups()
                
            return True
        except Exception as e:
            print(f"  error navigating: {e}")
            return False
    
    def _detect_cloudflare(self) -> bool:
        # detect if we're on a cloudflare challenge page
        try:
            page_content = self.page.content().lower()
            cloudflare_indicators = [
                'cloudflare',
                'checking your browser',
                'just a moment',
                'ddos protection',
                'ray id'
            ]
            return any(indicator in page_content for indicator in cloudflare_indicators)
        except:
            return False
    
    def _human_delay(self, min_sec: float = None, max_sec: float = None):
        # random delay to mimic human behavior
        min_sec = min_sec or self.min_delay
        max_sec = max_sec or self.max_delay
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def _dismiss_popups(self):
        # try to dismiss common popups, cookie banners, etc
        try:
            # common cookie banner and popup close buttons
            close_selectors = [
                'button:has-text("Accept")',
                'button:has-text("Accept All")',
                'button:has-text("I Agree")',
                'button:has-text("OK")',
                'button:has-text("Close")',
                '[aria-label="Close"]',
                '.close-button',
                '#onetrust-accept-btn-handler',  # common cookie consent
                '.cookie-accept',
                '[class*="cookie"] button',
                '[id*="cookie"] button'
            ]
            
            for selector in close_selectors:
                try:
                    button = self.page.query_selector(selector)
                    if button and button.is_visible():
                        print(f"  dismissing popup/banner...")
                        button.click()
                        time.sleep(0.5)
                        break
                except:
                    continue
        except:
            pass  # if popup dismissal fails, continue anyway
    
    def search_product(self, search_term: str) -> bool:
        # find search box and search for product
        try:
            print(f"  searching for: {search_term}")
            current_url = self.page.url.lower()
            
            # site-specific search logic
            if 'digikey' in current_url:
                return self._search_digikey(search_term)
            elif 'mouser' in current_url:
                return self._search_mouser(search_term)
            elif 'adafruit' in current_url:
                return self._search_adafruit(search_term)
            elif 'sparkfun' in current_url:
                return self._search_sparkfun(search_term)
            else:
                return self._search_generic(search_term)
            
        except Exception as e:
            print(f"  error searching: {e}")
            return False
    
    def _search_digikey(self, search_term: str) -> bool:
        # digikey-specific search with human-like behavior (cloudflare protected)
        try:
            # small random delay before interacting
            time.sleep(random.uniform(1, 2))
            
            # try to dismiss any popups first
            self._dismiss_popups()
            
            # digikey uses multiple possible selectors
            selectors = [
                '#searchInput',
                'input[data-testid="search-input"]',
                'input[id="searchInput"]',
                'input[name="keywords"]',
                'input[placeholder*="Part Number" i]',
                'input[type="text"][class*="search"]',
                '#searchform input',
                'header input[type="text"]'
            ]
            
            print(f"  looking for search box on digikey...")
            
            # take a screenshot for debugging
            if not self.headless:
                try:
                    self.page.screenshot(path='digikey_debug.png')
                    print(f"  screenshot saved to digikey_debug.png for debugging")
                except:
                    pass
            
            for i, selector in enumerate(selectors):
                try:
                    print(f"  trying selector {i+1}/{len(selectors)}: {selector}")
                    element = self.page.wait_for_selector(selector, timeout=3000)
                    if element and element.is_visible():
                        print(f"  ✓ found search box with: {selector}")
                        
                        # scroll to element if needed
                        element.scroll_into_view_if_needed()
                        time.sleep(0.5)
                        
                        # human-like interaction: click, wait, then type slowly
                        element.click()
                        time.sleep(random.uniform(0.5, 1.5))
                        
                        # clear any existing text
                        element.fill('')
                        
                        # type with random delays between keystrokes
                        typing_delay = random.randint(self.typing_delay_min, self.typing_delay_max)
                        print(f"  typing '{search_term}' with {typing_delay}ms delay...")
                        element.type(search_term, delay=typing_delay)
                        
                        # small pause before pressing enter
                        time.sleep(random.uniform(0.5, 1.0))
                        element.press('Enter')
                        
                        # wait for results (human-like delay)
                        delay = random.uniform(3, 5)
                        print(f"  search submitted, waiting {delay:.1f}s for results...")
                        time.sleep(delay)
                        
                        return True
                except Exception as e:
                    print(f"  selector {selector} failed: {str(e)[:50]}")
                    continue
            
            # if we get here, dump all input elements for debugging
            print(f"  ✗ no search box found, listing all input elements:")
            all_inputs = self.page.query_selector_all('input')
            for i, inp in enumerate(all_inputs[:10]):
                try:
                    if inp.is_visible():
                        print(f"    input {i}: id={inp.get_attribute('id')}, "
                              f"name={inp.get_attribute('name')}, "
                              f"class={inp.get_attribute('class')}, "
                              f"type={inp.get_attribute('type')}")
                except:
                    pass
            
            return False
        except Exception as e:
            print(f"  digikey search error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _search_mouser(self, search_term: str) -> bool:
        # mouser-specific search
        try:
            selectors = [
                'input[name="keyword"]',
                '#searchInput',
                'input[placeholder*="Search"]'
            ]
            
            for selector in selectors:
                try:
                    element = self.page.wait_for_selector(selector, timeout=3000)
                    if element and element.is_visible():
                        element.click()
                        element.fill(search_term)
                        element.press('Enter')
                        time.sleep(3)
                        print(f"  mouser search submitted")
                        return True
                except:
                    continue
            
            return False
        except:
            return False
    
    def _search_adafruit(self, search_term: str) -> bool:
        # adafruit-specific search
        try:
            selectors = [
                'input[name="q"]',
                '#search_query_top',
                'input[type="search"]'
            ]
            
            for selector in selectors:
                try:
                    element = self.page.wait_for_selector(selector, timeout=3000)
                    if element and element.is_visible():
                        element.click()
                        element.fill(search_term)
                        element.press('Enter')
                        time.sleep(3)
                        print(f"  adafruit search submitted")
                        return True
                except:
                    continue
            
            return False
        except:
            return False
    
    def _search_sparkfun(self, search_term: str) -> bool:
        # sparkfun-specific search
        try:
            selectors = [
                'input[name="q"]',
                '#search-input',
                'input[type="search"]'
            ]
            
            for selector in selectors:
                try:
                    element = self.page.wait_for_selector(selector, timeout=3000)
                    if element and element.is_visible():
                        element.click()
                        element.fill(search_term)
                        element.press('Enter')
                        time.sleep(3)
                        print(f"  sparkfun search submitted")
                        return True
                except:
                    continue
            
            return False
        except:
            return False
    
    def _search_generic(self, search_term: str) -> bool:
        # generic search for unknown sites with human-like behavior
        try:
            # small delay before searching
            time.sleep(random.uniform(1, 2))
            
            search_selectors = [
                'input[type="search"]',
                'input[name="search"]',
                'input[name="q"]',
                'input[id*="search" i]',
                'input[placeholder*="Search" i]',
                '#search-input',
                '.search-input',
                '[data-testid="search-input"]',
                'input[aria-label*="Search" i]'
            ]
            
            for selector in search_selectors:
                try:
                    element = self.page.wait_for_selector(selector, timeout=3000)
                    if element and element.is_visible():
                        # human-like: click, wait, type slowly
                        element.click()
                        time.sleep(random.uniform(0.3, 0.8))
                        
                        # type with varying speed
                        typing_delay = random.randint(80, 200)
                        element.type(search_term, delay=typing_delay)
                        
                        # pause before enter
                        time.sleep(random.uniform(0.3, 0.7))
                        element.press('Enter')
                        
                        # human-like wait for results
                        time.sleep(random.uniform(2.5, 4.0))
                        print(f"  search submitted")
                        return True
                except:
                    continue
            
            print(f"  no search box found")
            return False
            
        except Exception as e:
            print(f"  generic search error: {e}")
            return False
    
    def extract_product_info(self) -> Dict[str, Optional[str]]:
        # extract product information from search results page
        try:
            print(f"  extracting product info...")
            current_url = self.page.url.lower()
            
            # check for cloudflare challenge again
            if self._detect_cloudflare():
                print(f"  ⚠️  still on cloudflare challenge - consider using --show-browser")
                return {'product_name': None, 'price': None, 'product_url': None}
            
            # human-like wait for results to render
            delay = random.uniform(2, 4)
            time.sleep(delay)
            
            # site-specific extraction
            if 'digikey' in current_url:
                product_selectors = [
                    'tr[itemtype*="Product"]',
                    '.product-details',
                    '[data-testid="search-result-item"]',
                    'table.productlist tbody tr'
                ]
            elif 'mouser' in current_url:
                product_selectors = [
                    '.SearchResultsTableRow',
                    '.product-item',
                    'tr.search-result'
                ]
            elif 'adafruit' in current_url:
                product_selectors = [
                    '.product',
                    '.product-listing',
                    'li[class*="product"]'
                ]
            elif 'sparkfun' in current_url:
                product_selectors = [
                    '.product',
                    '.product-card',
                    'li[class*="product"]'
                ]
            else:
                # generic selectors
                product_selectors = [
                    '.product',
                    '.item',
                    '[data-product]',
                    '.search-result-item',
                    '.product-card',
                    '.product-item',
                    '[class*="product"]',
                    'tr[class*="result"]',
                    'li[class*="product"]'
                ]
            
            product_element = None
            for selector in product_selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    if elements and len(elements) > 0:
                        # get first visible product
                        for elem in elements[:5]:
                            try:
                                if elem.is_visible():
                                    product_element = elem
                                    break
                            except:
                                continue
                        if product_element:
                            print(f"  found product with selector: {selector}")
                            break
                except:
                    continue
            
            if not product_element:
                print(f"  no product found")
                return {'product_name': None, 'price': None, 'product_url': None}
            
            # extract product name
            product_name = None
            name_selectors = ['h2', 'h3', 'h4', '.title', '.name', '[class*="title"]', '[class*="name"]']
            for selector in name_selectors:
                try:
                    name_elem = product_element.query_selector(selector)
                    if name_elem:
                        product_name = name_elem.inner_text().strip()
                        if product_name:
                            break
                except:
                    continue
            
            # extract price
            price = None
            price_selectors = ['.price', '[class*="price"]', '[data-price]', 'span:has-text("$")']
            for selector in price_selectors:
                try:
                    price_elem = product_element.query_selector(selector)
                    if price_elem:
                        price_text = price_elem.inner_text().strip()
                        if '$' in price_text or any(c.isdigit() for c in price_text):
                            price = price_text
                            break
                except:
                    continue
            
            # extract product url
            product_url = None
            try:
                link_elem = product_element.query_selector('a')
                if link_elem:
                    href = link_elem.get_attribute('href')
                    if href:
                        # make absolute url if relative
                        if href.startswith('http'):
                            product_url = href
                        elif href.startswith('/'):
                            product_url = f"{self.page.url.split('/')[0]}//{self.page.url.split('/')[2]}{href}"
                        else:
                            product_url = f"{self.page.url.rsplit('/', 1)[0]}/{href}"
            except:
                pass
            
            print(f"  found: {product_name} - {price}")
            
            return {
                'product_name': product_name,
                'price': price,
                'product_url': product_url
            }
            
        except Exception as e:
            print(f"  error extracting product info: {e}")
            return {'product_name': None, 'price': None, 'product_url': None}
    
    def add_to_cart(self, product_url: str = None) -> Dict[str, any]:
        # navigate to product and add to cart
        try:
            if product_url:
                print(f"  navigating to product page...")
                self.page.goto(product_url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(2)
            
            print(f"  looking for add to cart button...")
            
            # try multiple add to cart button selectors
            cart_button_selectors = [
                'button:has-text("Add to Cart")',
                'button:has-text("Add to Basket")',
                'button:has-text("Add")',
                '[data-action="add-to-cart"]',
                '#add-to-cart',
                '.add-to-cart',
                'input[value*="Add to Cart"]',
                'button[name="add-to-cart"]'
            ]
            
            button_found = False
            for selector in cart_button_selectors:
                try:
                    button = self.page.wait_for_selector(selector, timeout=2000)
                    if button and button.is_visible():
                        button.click()
                        time.sleep(2)
                        button_found = True
                        print(f"  item added to cart!")
                        break
                except:
                    continue
            
            if not button_found:
                print(f"  could not find add to cart button")
                return {
                    'success': False,
                    'cart_url': None,
                    'message': 'Add to cart button not found'
                }
            
            # try to get cart url
            cart_url = None
            cart_link_selectors = [
                'a[href*="cart"]',
                'a[href*="basket"]',
                '.cart-link',
                '#cart-link',
                '[data-testid="cart-link"]'
            ]
            
            for selector in cart_link_selectors:
                try:
                    cart_link = self.page.query_selector(selector)
                    if cart_link:
                        cart_url = cart_link.get_attribute('href')
                        if cart_url and not cart_url.startswith('http'):
                            cart_url = f"{self.page.url.split('/')[0]}//{self.page.url.split('/')[2]}{cart_url}"
                        break
                except:
                    continue
            
            return {
                'success': True,
                'cart_url': cart_url,
                'message': 'Item added to cart successfully'
            }
            
        except Exception as e:
            print(f"  error adding to cart: {e}")
            return {
                'success': False,
                'cart_url': None,
                'message': str(e)
            }
    
    def get_current_url(self) -> str:
        # get current page url
        if self.page:
            return self.page.url
        return None
    
    def take_screenshot(self, path: str = "screenshot.png"):
        # take screenshot for debugging
        if self.page:
            self.page.screenshot(path=path)
            print(f"  screenshot saved to {path}")
    
    def close(self):
        # close browser and cleanup
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass

