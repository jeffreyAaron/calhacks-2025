# BOM to Order - Setup Guide

This guide will help you connect the frontend React application with the Python backend that processes BOM files.

## Architecture Overview

```
Frontend (React + Vite)
    ↓
Backend API (Flask)
    ↓
┌─────────────────────┬──────────────────────┐
│   csv_parser.py     │  gemini_seller.py    │
│   (Ollama LLM)      │  (Google Gemini)     │
└─────────────────────┴──────────────────────┘
```

## Prerequisites

### Backend Requirements
- Python 3.8+
- Ollama installed with `llama3.2:1b` model
- Google Gemini API key

### Frontend Requirements
- Node.js 18+
- pnpm (or npm)

## Setup Instructions

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Install and configure Ollama:
```bash
# Install Ollama from https://ollama.ai
# Then pull the required model
ollama pull llama3.2:1b
```

Add your Google Gemini API key:
```bash
# Create API_Key.txt in the project root directory
echo "YOUR_GEMINI_API_KEY" > ../API_Key.txt
```

Start the backend server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

Navigate to the frontend directory:
```bash
cd "BOM to Order/frontend"
```

Install dependencies:
```bash
pnpm install
# or
npm install
```

Configure the API URL (already set in `.env`):
```bash
VITE_API_URL=http://localhost:5000
```

Start the frontend development server:
```bash
pnpm dev
# or
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. **Upload BOM File**: Click to upload or drag-and-drop a CSV/Excel file containing your Bill of Materials
2. **Preview Data**: The uploaded file will be displayed in a table format
3. **Process BOM**: Click "Find Sellers" button to:
   - Parse the BOM using Ollama to extract part names and quantities
   - Query Google Gemini to find affordable seller links
4. **View Results**: Browse seller recommendations for each part

## API Endpoints

### `POST /api/process-bom`
Complete pipeline that:
1. Parses uploaded BOM file
2. Extracts part names and quantities using Ollama
3. Finds seller information using Google Gemini

**Request**: Form data with `file` field

**Response**:
```json
{
  "success": true,
  "parsed_data": [
    {"name": "Raspberry Pi 4", "quantity": 2}
  ],
  "seller_info": [
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

### `POST /api/parse-bom`
Parse BOM only (without seller lookup)

### `POST /api/get-sellers`
Get seller info for already parsed items

### `GET /health`
Health check endpoint

## Troubleshooting

### Backend Issues

**Ollama not found:**
- Ensure Ollama is installed and running
- Verify the model is pulled: `ollama list`

**Gemini API errors:**
- Check your API key in `API_Key.txt`
- Verify you have API quota remaining

**Import errors:**
- Ensure all dependencies are installed: `pip install -r backend/requirements.txt`

### Frontend Issues

**Cannot connect to backend:**
- Verify backend is running on port 5000
- Check CORS is enabled (already configured in Flask app)
- Verify `.env` has correct `VITE_API_URL`

**Build errors:**
- Clear node_modules and reinstall: `rm -rf node_modules && pnpm install`
- Check TypeScript errors: `pnpm run lint`

## Development Tips

- The backend uses temporary file storage for uploads
- Files are automatically cleaned up after processing
- Frontend supports CSV, TXT, XLSX, and XLS files
- Maximum file size: 16MB

## Production Deployment

### Backend
- Use a production WSGI server like Gunicorn:
  ```bash
  gunicorn -w 4 -b 0.0.0.0:5000 app:app
  ```
- Set appropriate CORS origins in production
- Store API keys securely (environment variables)

### Frontend
- Build for production:
  ```bash
  pnpm run build
  ```
- Update `VITE_API_URL` to production backend URL
- Deploy to Vercel, Netlify, or similar

## File Structure

```
calhacks-2025/
├── backend/
│   ├── app.py              # Flask API server
│   ├── csv_parser.py       # Ollama-based BOM parser
│   ├── gemini_seller.py    # Gemini-based seller lookup
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
├── BOM to Order/
│   └── frontend/
│       ├── src/
│       │   ├── lib/
│       │   │   └── api.ts          # API client
│       │   ├── components/
│       │   │   ├── SellerResults.tsx  # Seller display
│       │   │   ├── BOMPreview.tsx     # BOM table
│       │   │   └── FileUpload.tsx     # Upload component
│       │   └── pages/
│       │       └── Index.tsx          # Main page
│       ├── .env                    # Environment config
│       └── package.json
├── csv_parser.ipynb        # Original notebook
├── gemini_seller_info.ipynb # Original notebook
└── SETUP.md               # This file
```
