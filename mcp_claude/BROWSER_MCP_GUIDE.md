# Claude + Browser MCP Guide

This guide shows you how to use **Claude AI** with the **Browser MCP Chrome extension** to automate searching for BOM parts and adding them to your cart.

## What is Browser MCP?

Browser MCP is a Chrome extension that lets AI assistants like Claude control your browser through the Model Context Protocol (MCP). Instead of simulating browser actions, Claude can actually control your real Chrome browser!

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Your      │         │   Claude AI  │         │   Browser   │
│   Script    │────────▶│   (Anthropic)│────────▶│   MCP       │
│             │         │              │         │   Extension │
└─────────────┘         └──────────────┘         └─────────────┘
                                                         │
                                                         ▼
                                                  ┌─────────────┐
                                                  │   Chrome    │
                                                  │   Browser   │
                                                  └─────────────┘
```

## Setup Instructions

### 1. Install Browser MCP Extension

1. Open Chrome
2. Install the Browser MCP extension from the Chrome Web Store
3. Make sure the extension is enabled

### 2. Configure MCP Server

Your `~/.cursor/mcp.json` should have:

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

### 3. Install Python Dependencies

```bash
cd mcp_claude
pip install -r requirements.txt
```

### 4. Set Your Anthropic API Key

Get an API key from https://console.anthropic.com/

```bash
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

Or add to your `~/.zshrc` or `~/.bashrc`:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.zshrc
source ~/.zshrc
```

### 5. Test Your Setup

```bash
python test_browser_mcp.py
```

This will check:
- ✅ API key is set
- ✅ MCP config exists
- ✅ Python packages installed
- ✅ Claude API connection works

## Usage

### Basic Usage

```bash
python claude_with_browser_mcp.py example_bom.csv \
    --website https://www.adafruit.com
```

### With Output File

```bash
python claude_with_browser_mcp.py example_bom.csv \
    --website https://www.sparkfun.com \
    --output results.json
```

### All Options

```bash
python claude_with_browser_mcp.py example_bom.csv \
    --website https://www.digikey.com \
    --api-key sk-ant-... \
    --output my_results.json
```

## What Happens?

1. **📄 Reads your BOM CSV** - Parses part names, descriptions, quantities
2. **🤖 Claude analyzes each part** - Understands what to search for
3. **🌐 Opens browser** - Uses Browser MCP to control Chrome
4. **🔍 Searches for parts** - Navigates and searches intelligently
5. **💰 Finds prices** - Extracts product information
6. **🛒 Adds to cart** - Attempts to add each item
7. **📊 Returns results** - Structured data with all findings

## How Claude Uses Browser MCP

Claude has access to these browser tools:

| Tool | What It Does |
|------|--------------|
| `browser_navigate(url)` | Go to a URL |
| `browser_snapshot()` | See current page content |
| `browser_click(element, ref)` | Click an element |
| `browser_type(element, ref, text, submit)` | Type text |
| `browser_select_option(element, ref, values)` | Select dropdown option |
| `browser_press_key(key)` | Press keyboard key |
| `browser_screenshot()` | Take screenshot |
| `browser_wait(time)` | Wait for seconds |

Claude decides which tools to use and when, making intelligent decisions based on what it sees on the page.

## Example Workflow

```
User runs script with BOM
     ↓
Claude receives task: "Search for Arduino Uno R3"
     ↓
Claude: "I'll navigate to adafruit.com"
     ↓
Browser MCP: Opens Chrome → adafruit.com
     ↓
Claude: "Let me take a snapshot to see the page"
     ↓
Browser MCP: Returns page content
     ↓
Claude: "I see a search box, I'll search for the part"
     ↓
Browser MCP: Types "Arduino Uno R3" and submits
     ↓
Claude: "Let me check the results"
     ↓
Browser MCP: Returns search results page
     ↓
Claude: "I found it! Price is $24.95, clicking add to cart"
     ↓
Browser MCP: Clicks the button
     ↓
Claude reports back: "Success! Added to cart"
```

## BOM CSV Format

```csv
part_name,quantity,description
Arduino Uno R3,2,microcontroller board
HC-SR04 Ultrasonic Sensor,5,distance sensor
SG90 Servo Motor,3,9g micro servo
```

Required:
- `part_name` - What to search for

Optional:
- `quantity` - How many you need
- `description` - Extra context for Claude

## Recommended Websites

### ✅ Beginner-Friendly (No Bot Detection)
- **Adafruit.com** - Maker/hobbyist electronics
- **SparkFun.com** - Development boards, sensors

### ⚠️ Advanced (Has Cloudflare)
- **DigiKey.com** - Huge electronics catalog
- **Mouser.com** - Professional components

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### "Browser MCP not configured"
Check `~/.cursor/mcp.json` has the browsermcp server configured

### "Chrome not responding"
1. Make sure Chrome is running
2. Check Browser MCP extension is enabled
3. Try restarting Chrome

### Claude can't find elements
- Some websites have complex layouts
- Try a simpler website first (Adafruit, SparkFun)
- Claude will adapt and try different strategies

## Advanced: Programmatic Usage

```python
from claude_with_browser_mcp import ClaudeWithBrowserMCP

# Create instance
automation = ClaudeWithBrowserMCP()

# Search for a single part
result = automation.search_and_cart_part(
    part_name="Arduino Uno R3",
    description="microcontroller board",
    quantity="2",
    website_url="https://www.adafruit.com"
)

print(f"Found: {result['product_name']}")
print(f"Price: {result['price']}")

# Or process entire BOM
results = automation.process_bom(
    csv_file="my_bom.csv",
    website_url="https://www.sparkfun.com"
)
```

## Files in This Directory

```
mcp_claude/
├── claude_with_browser_mcp.py    # Main automation script
├── mcp_client.py                 # MCP protocol client
├── bom_parser.py                 # CSV parsing utility
├── test_browser_mcp.py           # Test your setup
├── example_bom.csv               # Sample BOM file
├── requirements.txt              # Python dependencies
├── BROWSER_MCP_GUIDE.md          # This file
└── SETUP.md                      # Alternative setup guide
```

## Tips for Success

1. **Start Simple** - Try Adafruit or SparkFun first
2. **Check Chrome** - Make sure browser and extension are working
3. **Watch Claude Work** - You'll see it think through problems
4. **Be Patient** - AI-controlled browsing takes time
5. **Iterate** - Claude learns what works on each site

## Getting Help

If you encounter issues:

1. Run the test script: `python test_browser_mcp.py`
2. Check your API key is valid
3. Verify Chrome and the extension are working
4. Try a simpler website first
5. Check console output for Claude's reasoning

## What Makes This Powerful?

Traditional browser automation breaks when websites change. **Claude + Browser MCP** adapts:

- 🧠 **Intelligent** - Claude understands context, not just scripts
- 🔄 **Adaptive** - Works across different website layouts
- 🎯 **Goal-Oriented** - Focused on outcomes, not rigid steps
- 🤝 **Interactive** - Can handle popups, dialogs, variations
- 📊 **Informative** - Explains what it's doing and why

## Next Steps

1. ✅ Test your setup: `python test_browser_mcp.py`
2. ✅ Try the example: `python claude_with_browser_mcp.py example_bom.csv`
3. ✅ Use your own BOM: `python claude_with_browser_mcp.py your_bom.csv`
4. ✅ Automate your workflow!

---

Happy automating! 🚀

