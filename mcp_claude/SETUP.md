# Claude Browser MCP - Setup Guide

This directory contains code to use **Claude AI** with the **Browser MCP Chrome extension** to intelligently control a browser and automate searching for parts from a Bill of Materials (BOM) CSV file.

## Features

✅ **Claude-Powered Intelligence**: Uses Claude 3.5 Sonnet to understand web pages and make smart decisions  
✅ **Real Browser Control**: Uses Browser MCP Chrome extension (not simulation!)  
✅ **BOM Processing**: Reads parts from CSV and searches for them automatically  
✅ **Price Extraction**: Finds product prices on websites  
✅ **Add to Cart**: Attempts to add items to shopping cart  
✅ **Multi-Website Support**: Works with various electronics suppliers  
✅ **Adaptive**: Claude adapts to different website layouts  

## Prerequisites

1. **Python 3.8+**
2. **Anthropic API Key** - Get one at https://console.anthropic.com/
3. **Browser MCP Chrome Extension** - Installed in Chrome
4. **MCP Server** - Configured in `~/.cursor/mcp.json`

## Installation

### 1. Install Browser MCP Chrome Extension

Install the Browser MCP extension from the Chrome Web Store and make sure it's enabled.

### 2. Configure MCP Server

Make sure your `~/.cursor/mcp.json` contains:

```json
{
  "mcpServers": {
    "browsermcp": {
      "command": "npx",
      "args": ["@browsermcp/mcp@latest"]
    }
  }
}
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Anthropic API key

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or add it to your `~/.bashrc` or `~/.zshrc` to make it permanent:

```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 5. Test Your Setup

```bash
./quick_start.sh
```

Or manually:

```bash
python test_browser_mcp.py
```

## Quick Start

### Option 1: Quick Start Script (Recommended)

```bash
./quick_start.sh
```

This will check your setup and guide you through running the automation.

### Option 2: Direct Command

```bash
python claude_with_browser_mcp.py example_bom.csv \
    --website https://www.adafruit.com
```

### Option 3: With Output File

```bash
python claude_with_browser_mcp.py example_bom.csv \
    --website https://www.sparkfun.com \
    --output results.json
```

#### Available Options:

- `--website URL` - Website to search on (default: adafruit.com)
- `--api-key KEY` - Override ANTHROPIC_API_KEY environment variable
- `--output FILE` - Save results to JSON file

## BOM CSV Format

Your CSV file should have these columns:

```csv
part_name,quantity,description
Arduino Uno R3,2,microcontroller board
HC-SR04 Ultrasonic Sensor,5,distance sensor
```

Required columns:
- `part_name` - The name of the part to search for

Optional columns:
- `quantity` - How many you need
- `description` - Additional context for better search results

## Recommended Websites

### Easy (No Anti-Bot Protection)
- ✅ **Adafruit.com** - Great for maker/hobbyist electronics
- ✅ **SparkFun.com** - Good for development boards and sensors

### Challenging (Has Cloudflare)
- ⚠️ **DigiKey.com** - Huge selection, but harder to automate
- ⚠️ **Mouser.com** - Huge selection, but harder to automate

**Tip**: For Cloudflare-protected sites, do NOT use `--headless` mode. The visible browser is better at bypassing bot detection.

## How It Works

1. **Parse BOM**: Reads your CSV file to get part names and descriptions
2. **Claude Analyzes**: Claude looks at each part and determines the best search strategy
3. **Browser Control**: Playwright automates the browser to:
   - Navigate to the website
   - Search for the part
   - Extract product information
   - Find prices
   - Add to cart
4. **Results**: Returns structured data with product names, prices, URLs, and cart status

## Example Output

```
🔍 Searching for 'Arduino Uno R3' on https://www.adafruit.com
🤖 Claude suggests searching for: Arduino Uno R3 microcontroller
✅ Found: Arduino Uno R3 - $24.95
🛒 Adding Arduino Uno R3 to cart...
✅ Added to cart successfully!
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Make sure you've set the environment variable:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### "playwright install required"
Install browser binaries:
```bash
playwright install chromium
```

### "Cloudflare challenge detected"
Don't use `--headless` mode. Run with visible browser:
```bash
python simple_example.py  # Already uses visible mode
```

### Browser won't start
Make sure Playwright is properly installed:
```bash
pip install playwright
playwright install chromium
```

## Code Structure

```
mcp_claude/
├── claude_browser_automation.py  # Main Claude automation class
├── playwright_mcp_bridge.py      # Browser control wrapper
├── bom_parser.py                 # CSV parsing utilities
├── simple_example.py             # Simple usage example
├── run_claude_example.sh         # Bash script for easy running
├── example_bom.csv               # Sample BOM file
├── requirements.txt              # Python dependencies
└── SETUP.md                      # This file
```

## Programmatic Usage

```python
from claude_browser_automation import ClaudeBrowserAutomation

# Create automation instance
automation = ClaudeBrowserAutomation(
    api_key="your-key",  # Or use ANTHROPIC_API_KEY env var
    headless=False       # Show browser window
)

# Process BOM file
results = automation.process_bom_parts(
    csv_file="my_bom.csv",
    website_url="https://www.adafruit.com"
)

# Access results
for result in results:
    print(f"Part: {result['bom_part_name']}")
    print(f"Found: {result['product_name']}")
    print(f"Price: {result['price']}")
    print(f"URL: {result['product_url']}")
```

## License

MIT License - Feel free to use and modify as needed!

