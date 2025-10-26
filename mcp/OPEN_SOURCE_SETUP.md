# open source model setup guide

this guide shows how to use open source models with the bom ordering system instead of openai.

## quick start with ollama

### 1. install ollama
```bash
# macos/linux
curl -fsSL https://ollama.ai/install.sh | sh

# or download from https://ollama.ai
```

### 2. pull a model
```bash
# recommended models for this task:
ollama pull llama3.1        # best balance of quality and speed
ollama pull mistral          # faster, good quality
ollama pull codellama        # optimized for structured output
ollama pull llama3.1:70b     # highest quality (requires more ram)
```

### 3. verify ollama is running
```bash
# check if ollama server is running
curl http://localhost:11434/api/tags

# if not running, start it
ollama serve
```

### 4. configure the app
edit your `.env` file:
```bash
# gemini still needed for website discovery
GEMINI_API_KEY=your_gemini_key

# enable open source mode
USE_OPEN_SOURCE_MODEL=true
OPEN_SOURCE_BASE_URL=http://localhost:11434/v1
OPEN_SOURCE_MODEL_NAME=llama3.1
```

### 5. run the app
```bash
python main.py example_bom.csv --use-open-source
```

## alternative: lm studio

### 1. install lm studio
download from https://lmstudio.ai

### 2. load a model
- open lm studio
- search for models (llama, mistral, etc)
- download your preferred model
- click "start server" in the local server tab

### 3. configure
```bash
USE_OPEN_SOURCE_MODEL=true
OPEN_SOURCE_BASE_URL=http://localhost:1234/v1
OPEN_SOURCE_MODEL_NAME=<model-name-from-lm-studio>
```

## model recommendations

### for browser automation tasks:
1. **llama3.1** (8b) - best all-around choice
   - good at following instructions
   - handles json output well
   - reasonable speed

2. **mistral** (7b) - faster alternative
   - good instruction following
   - faster inference
   - slightly less accurate

3. **llama3.1:70b** - highest quality
   - best accuracy
   - better reasoning
   - requires 40gb+ ram
   - slower inference

### command line override
you can override env settings with command line args:
```bash
# use specific model
python main.py example_bom.csv --use-open-source --model-name mistral

# use custom endpoint
python main.py example_bom.csv --use-open-source \
  --base-url http://my-server:8000/v1 \
  --model-name my-custom-model
```

## performance comparison

| model | speed | accuracy | memory |
|-------|-------|----------|--------|
| llama3.1:8b | fast | high | 8gb |
| mistral:7b | very fast | good | 6gb |
| llama3.1:70b | slow | very high | 40gb |
| codellama:13b | medium | high | 12gb |

## troubleshooting

### ollama not responding
```bash
# restart ollama
pkill ollama
ollama serve
```

### model not found
```bash
# list available models
ollama list

# pull the model
ollama pull llama3.1
```

### connection refused
```bash
# verify ollama is running
curl http://localhost:11434/api/tags

# check the base url in your config matches
```

### poor quality results
- try a larger model (e.g., llama3.1:70b)
- reduce temperature in browser_controller.py
- provide more detailed prompts
- use instruction-tuned models

## cost comparison

### openai (gpt-4)
- ~$0.03 per 1k tokens input
- ~$0.06 per 1k tokens output
- typical bom with 10 parts × 3 websites = ~$5-10

### open source (local)
- $0 per request
- one-time hardware cost
- requires ~8-40gb ram depending on model
- slower but free unlimited usage


