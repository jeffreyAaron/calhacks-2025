# Backend API Server

This Flask API server connects the Python processing scripts to the frontend.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is installed and running with the `llama3.2:1b` model:
```bash
ollama pull llama3.2:1b
```

3. Create an `API_Key.txt` file in the parent directory with your Google Gemini API key, or pass it in API requests.

## Running the Server

```bash
python app.py
```

The server will run on `http://localhost:5000`

## API Endpoints

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### `POST /api/parse-bom`
Parse uploaded BOM file and extract part names and quantities using Ollama.

**Request:** 
- Form data with `file` field containing CSV/XLSX file

**Response:**
```json
{
  "success": true,
  "data": [
    {"name": "Raspberry Pi 4", "quantity": 2},
    {"name": "Arduino Uno", "quantity": 5}
  ]
}
```

### `POST /api/get-sellers`
Get seller information for parsed BOM items using Google Gemini.

**Request:**
```json
{
  "items": [
    {"name": "Raspberry Pi 4", "quantity": 2}
  ],
  "api_key": "optional-api-key"
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "Raspberry Pi 4",
      "quantity": 2,
      "sellers": [
        {"company": "Adafruit", "link": "https://adafruit.com"},
        {"company": "SparkFun", "link": "https://sparkfun.com"}
      ]
    }
  ]
}
```

### `POST /api/process-bom`
Complete pipeline: parse BOM and get seller info in one request.

**Request:**
- Form data with `file` field containing CSV/XLSX file

**Response:**
```json
{
  "success": true,
  "parsed_data": [...],
  "seller_info": [...]
}
```
