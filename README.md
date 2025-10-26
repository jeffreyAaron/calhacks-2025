# calhacks-2025
MCP BOM Ordering

an agentic ai app that streamlines and automates ordering parts from a bill of materials (bom)

## overview

this app uses ai agents to:
1. parse a bom csv file
2. find relevant supplier websites using gemini api
3. control browsers via mcp protocol with chatgpt to search for parts and prices
4. add parts to shopping carts automatically
5. export results with pricing and links back to csv

## setup

1. install dependencies:
```bash
pip install -r requirements.txt

# install playwright browsers
playwright install chromium

# or use the setup script
./setup_playwright.sh
```

2. set up api keys:
   - copy `.env.example` to `.env`
   - add your gemini api key
   - choose between openai or open source models (see below)
   - configure mcp server url (if needed)

3. ensure mcp server is running for browser automation

### using openai (default)
set in `.env`:
```
OPENAI_API_KEY=your_key_here
OPENAI_MODEL_NAME=gpt-4
```

### using open source models
this app supports any openai-compatible api (ollama, lm studio, vllm, etc.)

**option 1: ollama**
1. install ollama from https://ollama.ai
2. pull a model: `ollama pull llama3.1`
3. set in `.env`:
```
USE_OPEN_SOURCE_MODEL=true
OPEN_SOURCE_BASE_URL=http://localhost:11434/v1
OPEN_SOURCE_MODEL_NAME=llama3.1
```

**option 2: lm studio**
1. install lm studio from https://lmstudio.ai
2. load a model and start the server
3. set in `.env`:
```
USE_OPEN_SOURCE_MODEL=true
OPEN_SOURCE_BASE_URL=http://localhost:1234/v1
OPEN_SOURCE_MODEL_NAME=your-model-name
```

**option 3: any openai-compatible endpoint**
```
USE_OPEN_SOURCE_MODEL=true
OPEN_SOURCE_BASE_URL=http://your-endpoint/v1
OPEN_SOURCE_MODEL_NAME=your-model-name
OPEN_SOURCE_API_KEY=your-key-if-needed
```

## usage

run the automated ordering system:

```bash
python main.py path/to/your/bom.csv
```

options:
- `--num-websites N`: number of websites to search per part (default: 3)
- `--output FILE`: specify output csv file path
- `--gemini-key KEY`: provide gemini api key directly
- `--openai-key KEY`: provide openai api key directly
- `--use-open-source`: use open source model instead of openai
- `--model-name NAME`: specify model name (e.g., llama3.1, gpt-4)
- `--base-url URL`: specify base url for model api
- `--show-browser`: show browser window (watch automation happen)
- `--headless`: run browser in background (faster, invisible)
- `--no-browser`: use llm simulation instead of real browser

examples:
```bash
# recommended: visible browser (avoids cloudflare/bot detection)
python main.py example_bom.csv --show-browser

# with open source model and visible browser
python main.py example_bom.csv --use-open-source --show-browser

# headless mode (⚠️ may be detected by cloudflare on digikey/mouser)
python main.py example_bom.csv --headless

# headless with more websites (not recommended for protected sites)
python main.py example_bom.csv --headless --num-websites 5

# llm simulation only (no real browser)
python main.py example_bom.csv --no-browser
```

**important:** digikey and mouser use cloudflare protection. for best results:
- use `--show-browser` (visible mode)
- headless mode will likely be blocked
- see `ANTI_DETECTION.md` for details

## how it works

### step 1: bom parsing (`bom_parser.py`)
parses the input csv and extracts part information

### step 2: website discovery (`website_finder.py`)
uses gemini api to find relevant supplier websites for each part

### step 3: browser automation (`browser_controller.py` + `playwright_mcp_bridge.py`)
uses playwright to actually control a real browser:
- opens chromium browser (visible or headless)
- navigates to supplier websites
- searches for parts using real search forms
- extracts actual pricing and product urls from live pages
- adds items to real shopping carts

can run in visible mode (watch it work) or headless mode (faster)

### step 4: results compilation (`csv_updater.py`)
appends search results to the original csv with new columns:
- website
- product_name_found
- product_url
- price
- cart_url
- added_to_cart

## example bom format

```csv
part_name,quantity,description
Arduino Uno R3,2,microcontroller board
HC-SR04 Ultrasonic Sensor,5,distance sensor
```

the system works with various csv formats and automatically detects the part name column.
