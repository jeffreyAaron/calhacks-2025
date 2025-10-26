# quickstart: using open source models

complete walkthrough to get the bom ordering system running with free, local open source models.

## option 1: ollama (recommended)

### step 1: install ollama

**macos:**
```bash
brew install ollama
```

**linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**windows:**
download from https://ollama.ai/download

### step 2: start ollama and pull a model

```bash
# start ollama service (if not already running)
ollama serve &

# pull llama3.1 (recommended for this task)
ollama pull llama3.1

# verify it's working
ollama run llama3.1 "hello"
```

### step 3: install python dependencies

```bash
cd /Users/jeffrey/Documents/Coding/github/calhacks-2025
pip install -r requirements.txt
```

### step 4: set up your api keys

create a `.env` file:
```bash
# gemini api key (still needed for website discovery)
GEMINI_API_KEY=your_gemini_api_key_here

# enable open source mode
USE_OPEN_SOURCE_MODEL=true
OPEN_SOURCE_BASE_URL=http://localhost:11434/v1
OPEN_SOURCE_MODEL_NAME=llama3.1
OPEN_SOURCE_API_KEY=not-needed
```

**get gemini api key:**
1. go to https://makersuite.google.com/app/apikey
2. click "create api key"
3. copy and paste into `.env` file

### step 5: run the system!

```bash
# run with default settings (3 websites per part)
python main.py example_bom.csv --use-open-source

# or specify more websites
python main.py example_bom.csv --use-open-source --num-websites 5

# or with custom output file
python main.py example_bom.csv --use-open-source --output my_results.csv
```

### step 6: check the results

the system will create a file like `example_bom_updated.csv` with:
- all original columns from your bom
- new columns: website, product_name_found, product_url, price, cart_url, added_to_cart

## option 2: lm studio (gui alternative)

### step 1: install lm studio

download from https://lmstudio.ai

### step 2: download a model

1. open lm studio
2. click "search" tab
3. search for "llama-3.1-8b-instruct"
4. click download

### step 3: start the local server

1. click "local server" tab (chat bubble icon)
2. select your downloaded model
3. click "start server"
4. note the url (usually http://localhost:1234/v1)

### step 4: configure and run

create `.env`:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
USE_OPEN_SOURCE_MODEL=true
OPEN_SOURCE_BASE_URL=http://localhost:1234/v1
OPEN_SOURCE_MODEL_NAME=llama-3.1-8b-instruct
```

run:
```bash
python main.py example_bom.csv --use-open-source
```

## testing without mcp (simplified test)

if you want to test just the llm connection without full mcp setup:

```python
# test_opensource.py
from browser_controller import BrowserController

# initialize with open source
controller = BrowserController(
    use_open_source=True,
    model_name="llama3.1",
    base_url="http://localhost:11434/v1"
)

# test it
result = controller.search_part_on_website(
    "Arduino Uno R3", 
    "https://www.digikey.com"
)

print(result)
```

run:
```bash
python test_opensource.py
```

## using your own bom file

### step 1: prepare your csv

your csv should have at least a column with part names:
```csv
part_name,quantity,description
Resistor 10k ohm,100,1/4W resistor
Capacitor 100uF,50,electrolytic capacitor
Arduino Nano,5,microcontroller
```

supported column names:
- `part_name`, `Part Name`, `part`, `Part`
- `description`, `Description`
- `item`, `Item`

### step 2: run with your file

```bash
python main.py /path/to/your/bom.csv --use-open-source --output results.csv
```

## example output

running the system will show:
```
=== bom automated ordering system ===

step 1: parsing bom csv...
found 6 parts in bom

step 2: finding relevant websites using gemini...
finding websites for: Arduino Uno R3
finding websites for: HC-SR04 Ultrasonic Sensor
...
found websites for all parts

step 3: searching parts on websites and adding to cart...

processing: Arduino Uno R3
  searching Arduino Uno R3 on https://www.digikey.com
  searching Arduino Uno R3 on https://www.mouser.com
  searching Arduino Uno R3 on https://www.adafruit.com

processing: HC-SR04 Ultrasonic Sensor
  searching HC-SR04 Ultrasonic Sensor on https://www.digikey.com
  ...

step 4: updating csv with results...
updated csv saved to: example_bom_updated.csv

=== process complete ===
results saved to: example_bom_updated.csv
```

## model recommendations by task

**for 1-10 parts (small boms):**
- llama3.1:8b (good balance)
- mistral:7b (faster)

**for 10-50 parts (medium boms):**
- llama3.1:8b (consistent quality)

**for 50+ parts (large boms):**
- mistral:7b (speed priority)
- or use openai gpt-4 (remove --use-open-source flag)

## cost comparison example

**processing 20 parts × 3 websites = 60 searches:**

| provider | cost | speed | quality |
|----------|------|-------|---------|
| openai gpt-4 | ~$10-15 | fast | excellent |
| llama3.1 (local) | $0 | medium | very good |
| mistral (local) | $0 | fast | good |

## troubleshooting

### "connection refused" error
```bash
# make sure ollama is running
curl http://localhost:11434/api/tags

# if not, start it
ollama serve
```

### "model not found" error
```bash
# list your models
ollama list

# pull the model
ollama pull llama3.1
```

### gemini api error
- verify your gemini api key is correct
- check you have api access enabled at https://makersuite.google.com

### slow performance
```bash
# try a smaller/faster model
python main.py example_bom.csv --use-open-source --model-name mistral

# or reduce websites per part
python main.py example_bom.csv --use-open-source --num-websites 2
```

## next steps

1. test with the example bom: `example_bom.csv`
2. try with your own bom file
3. experiment with different models
4. adjust number of websites based on your needs
5. set up mcp server for full browser automation

for full mcp setup, see the main README.md


