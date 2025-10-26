# 🤖 Claude + Browser MCP Automation

Automate searching for BOM (Bill of Materials) parts using **Claude AI** with the **Browser MCP Chrome extension**. Claude intelligently controls your Chrome browser to search for parts, find prices, and add items to cart.

## ✨ What This Does

1. **📄 Reads your BOM CSV** - Parses electronic component names
2. **🧠 Claude analyzes** - AI understands what to search for
3. **🌐 Opens browser** - Controls real Chrome via Browser MCP
4. **🔍 Searches intelligently** - Adapts to different websites
5. **💰 Finds prices** - Extracts product information
6. **🛒 Adds to cart** - Attempts to purchase items
7. **📊 Reports results** - Returns structured data

## 🚀 Quick Start

```bash
# 1. Test your setup
./quick_start.sh

# 2. Run the automation
python claude_with_browser_mcp.py example_bom.csv --website https://www.adafruit.com

# 3. Check the results!
```

## 📋 Prerequisites

Before you begin, you need:

- ✅ **Python 3.8+**
- ✅ **Anthropic API Key** - Get from [console.anthropic.com](https://console.anthropic.com/)
- ✅ **Browser MCP Extension** - Installed in Chrome
- ✅ **MCP Config** - Set up in `~/.cursor/mcp.json`

## 📦 Installation

### Step 1: Set API Key

```bash
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Test Setup

```bash
python test_browser_mcp.py
```

## 💻 Usage Examples

### Basic Usage

```bash
python claude_with_browser_mcp.py example_bom.csv
```

### Specify Website

```bash
python claude_with_browser_mcp.py example_bom.csv \
    --website https://www.sparkfun.com
```

### Save Results

```bash
python claude_with_browser_mcp.py example_bom.csv \
    --website https://www.adafruit.com \
    --output results.json
```

### Use Your Own BOM

```bash
python claude_with_browser_mcp.py my_parts.csv \
    --website https://www.digikey.com \
    --output my_results.json
```

## 📄 BOM CSV Format

Create a CSV file like this:

```csv
part_name,quantity,description
Arduino Uno R3,2,microcontroller board
HC-SR04 Ultrasonic Sensor,5,distance sensor
SG90 Servo Motor,3,9g micro servo
```

**Required:**
- `part_name` - The component name

**Optional:**
- `quantity` - How many you need
- `description` - Extra context for better search results

## 🌐 Supported Websites

### ✅ Easy (Recommended for First Try)
- **[Adafruit.com](https://www.adafruit.com)** - Maker/hobbyist electronics
- **[SparkFun.com](https://www.sparkfun.com)** - Development boards

### ⚠️ Advanced (Has Bot Protection)
- **[DigiKey.com](https://www.digikey.com)** - Huge catalog
- **[Mouser.com](https://www.mouser.com)** - Professional components

## 📁 Files in This Directory

| File | Purpose |
|------|---------|
| `claude_with_browser_mcp.py` | ⭐ Main script - Run this! |
| `test_browser_mcp.py` | 🧪 Test your setup |
| `quick_start.sh` | 🚀 One-click setup check |
| `mcp_client.py` | 🔌 MCP protocol client |
| `bom_parser.py` | 📊 CSV parsing utility |
| `example_bom.csv` | 📝 Sample BOM file |
| `requirements.txt` | 📦 Python dependencies |
| `BROWSER_MCP_GUIDE.md` | 📚 Detailed guide |
| `SETUP.md` | ⚙️ Setup instructions |

## 🎯 How It Works

```
┌─────────────────┐
│  Your BOM CSV   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐      ┌─────────────┐
│   Python        │─────▶│   Claude AI  │─────▶│   Browser   │
│   Script        │      │   (Sonnet)   │      │   MCP       │
└─────────────────┘      └──────────────┘      └──────┬──────┘
                                                       │
                                                       ▼
                                                ┌─────────────┐
                                                │   Chrome    │
                                                │   Browser   │
                                                └─────────────┘
```

### Claude's Available Tools

When searching, Claude can use these browser tools:

- `browser_navigate(url)` - Go to a webpage
- `browser_snapshot()` - See what's on the page
- `browser_click(element, ref)` - Click buttons/links
- `browser_type(element, ref, text, submit)` - Fill in forms
- `browser_select_option(element, ref, values)` - Use dropdowns
- `browser_screenshot()` - Take screenshots
- `browser_wait(time)` - Wait for page loads

Claude **decides which tools to use** based on what it sees!

## 🔧 Troubleshooting

### "ANTHROPIC_API_KEY not found"

```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### "Browser MCP not configured"

Check `~/.cursor/mcp.json`:

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

### Chrome not responding

1. Make sure Chrome is running
2. Check Browser MCP extension is enabled
3. Try restarting Chrome

### Can't find elements on page

- Try a simpler website first (Adafruit, SparkFun)
- Claude will adapt and try different strategies
- Check console output to see Claude's reasoning

## 📖 Example Output

```
╔════════════════════════════════════════════════════════════════╗
║          🤖 Claude + Browser MCP Integration                  ║
╚════════════════════════════════════════════════════════════════╝

📄 Reading BOM from: example_bom.csv
🌐 Target website: https://www.adafruit.com

✅ Found 3 parts to process

======================================================================
🔢 Processing Part 1/3
======================================================================
🔍 Part: Arduino Uno R3
📝 Description: microcontroller board
📦 Quantity: 2
🌐 Website: https://www.adafruit.com
======================================================================

🤖 Asking Claude to search for the part...
🤖 Claude's Response:
I'll help you search for the Arduino Uno R3. Let me navigate to Adafruit...
[Claude searches and finds the product]
✅ Found: Arduino Uno R3 - $24.95
🛒 Added to cart successfully!

======================================================================
📊 FINAL SUMMARY
======================================================================

📦 Total parts processed: 3
✅ Products found: 3
🛒 Added to cart: 3
❌ Errors: 0
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Quick setup test
./quick_start.sh

# Detailed test
python test_browser_mcp.py
```

## 📚 Documentation

- **[BROWSER_MCP_GUIDE.md](./BROWSER_MCP_GUIDE.md)** - Complete guide with examples
- **[SETUP.md](./SETUP.md)** - Detailed setup instructions

## 🎓 Advanced Usage

### Programmatic API

```python
from claude_with_browser_mcp import ClaudeWithBrowserMCP

# Create automation instance
automation = ClaudeWithBrowserMCP()

# Search for a single part
result = automation.search_and_cart_part(
    part_name="Arduino Uno R3",
    description="microcontroller",
    quantity="2",
    website_url="https://www.adafruit.com"
)

# Or process entire BOM
results = automation.process_bom(
    csv_file="my_bom.csv",
    website_url="https://www.sparkfun.com"
)
```

## 🌟 Why This is Cool

**Traditional automation** breaks when websites change.  
**Claude + Browser MCP** adapts:

- 🧠 **Intelligent** - Understands context, not just scripts
- 🔄 **Adaptive** - Works with layout changes
- 🎯 **Goal-oriented** - Focused on outcomes
- 🤝 **Interactive** - Handles popups and variations
- 📊 **Transparent** - Shows you what it's doing

## 🤝 Contributing

Found a bug? Have an idea? Contributions welcome!

## 📄 License

MIT License - Use freely!

---

**Ready to automate?** Start with `./quick_start.sh` and let Claude do the work! 🚀

