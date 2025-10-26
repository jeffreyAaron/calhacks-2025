# BOM to Order

An intelligent Bill of Materials (BOM) processing application that automatically extracts part information from uploaded files and finds affordable seller recommendations.

## Features

- 📄 **Multi-format Support**: Upload CSV, Excel, or text files
- 🤖 **AI-Powered Parsing**: Uses Ollama LLM to intelligently extract part names and quantities
- 🔍 **Smart Seller Lookup**: Leverages Google Gemini to find affordable sellers for each part
- 💻 **Modern UI**: Clean, responsive React interface with real-time previews
- 🚀 **Complete Pipeline**: Seamless integration from upload to seller recommendations

## Quick Start

# 1. Install prerequisites (if not already)
# - Ollama: https://ollama.ai
# - Pull model: ollama pull llama3.2:1b
# - Create API_Key.txt with your Gemini API key


### Option 1: Automated Startup (Recommended)

```bash
# Using bash script
./start.sh

# Or using Python script
python start.py
```

### Option 2: Manual Setup

See [SETUP.md](SETUP.md) for detailed instructions.

**Quick summary:**

1. **Backend Setup**:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

2. **Frontend Setup**:
```bash
cd "BOM to Order/frontend"
pnpm install
pnpm dev
```

3. **Access**:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:5000

## Prerequisites

- Python 3.8+
- Node.js 18+
- Ollama (with `llama3.2:1b` model)
- Google Gemini API key (in `API_Key.txt`)

## Architecture

```
┌─────────────────────────────────────┐
│   React Frontend (Vite + TypeScript)│
│   - File upload & preview           │
│   - Results display                 │
└──────────────┬──────────────────────┘
               │ HTTP API
┌──────────────▼──────────────────────┐
│   Flask Backend (Python)            │
│   - API endpoints                   │
│   - File processing                 │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
┌─────────────┐   ┌──────────────┐
│ csv_parser  │   │ gemini_seller│
│  (Ollama)   │   │  (Gemini AI) │
└─────────────┘   └──────────────┘
```

## Project Structure

```
calhacks-2025/
├── backend/                 # Flask API server
│   ├── app.py              # Main API server
│   ├── csv_parser.py       # BOM parsing with Ollama
│   ├── gemini_seller.py    # Seller lookup with Gemini
│   └── requirements.txt    # Python dependencies
├── BOM to Order/
│   └── frontend/           # React frontend
│       ├── src/
│       │   ├── components/ # UI components
│       │   ├── lib/        # API client
│       │   └── pages/      # Page components
│       └── package.json
├── csv_parser.ipynb        # Original parsing notebook
├── gemini_seller_info.ipynb # Original seller lookup notebook
├── start.sh                # Bash startup script
├── start.py                # Python startup script
├── SETUP.md               # Detailed setup guide
└── README.md              # This file
```

## Usage

1. **Upload BOM File**: Drag and drop or click to upload your BOM file (CSV, XLSX, or TXT)
2. **Preview**: Review the uploaded data in table format
3. **Process**: Click "Find Sellers" to run the AI pipeline
4. **Results**: View seller recommendations with direct links

## API Documentation

See [backend/README.md](backend/README.md) for complete API documentation.

### Key Endpoints

- `POST /api/process-bom` - Complete pipeline (parse + seller lookup)
- `POST /api/parse-bom` - Parse BOM only
- `POST /api/get-sellers` - Get sellers for parsed items
- `GET /health` - Health check

## Development

### Backend Development

```bash
cd backend
python app.py  # Runs on http://localhost:5000
```

### Frontend Development

```bash
cd "BOM to Order/frontend"
pnpm dev  # Runs on http://localhost:5173
```

## Troubleshooting

See [SETUP.md](SETUP.md#troubleshooting) for common issues and solutions.

## Technologies

**Frontend:**
- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui components
- React Query

**Backend:**
- Flask
- pandas
- Ollama (llama3.2:1b)
- Google Generative AI (Gemini)

## License

MIT

## Contributors

Created for CalHacks 2025

