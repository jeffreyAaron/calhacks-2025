# System Architecture Diagram

## High-Level Overview

```
┌────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                           │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │          React Frontend (Port 5173)                   │    │
│  │                                                        │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │    │
│  │  │ FileUpload   │  │ BOMPreview   │  │  Seller    │ │    │
│  │  │  Component   │  │  Component   │  │  Results   │ │    │
│  │  └──────┬───────┘  └──────────────┘  └────────────┘ │    │
│  │         │                                             │    │
│  │         │  ┌──────────────────────────────────────┐  │    │
│  │         └──│  API Client (lib/api.ts)             │  │    │
│  │            └──────────────┬───────────────────────┘  │    │
│  └───────────────────────────┼──────────────────────────┘    │
└────────────────────────────┼─┼──────────────────────────────┘
                              │ │
                    HTTP API  │ │  JSON Response
                              ▼ │
┌────────────────────────────────▼──────────────────────────────┐
│              Flask Backend (Port 5000)                         │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                    app.py                             │    │
│  │                                                        │    │
│  │  ┌──────────────────┐  ┌──────────────────────────┐ │    │
│  │  │ /api/parse-bom   │  │ /api/get-sellers         │ │    │
│  │  │                  │  │                          │ │    │
│  │  │ /api/process-bom │  │ /health                  │ │    │
│  │  └────────┬─────────┘  └────────┬─────────────────┘ │    │
│  └───────────┼──────────────────────┼────────────────────┘    │
│              │                      │                         │
│              ▼                      ▼                         │
│  ┌────────────────────┐  ┌──────────────────────────┐       │
│  │  csv_parser.py     │  │  gemini_seller.py        │       │
│  │                    │  │                          │       │
│  │  • process_csv()   │  │  • get_seller_info()     │       │
│  │  • parse_row()     │  │  • prompt_gemini()       │       │
│  └─────────┬──────────┘  └───────────┬──────────────┘       │
└────────────┼──────────────────────────┼─────────────────────┘
             │                          │
             │                          │
             ▼                          ▼
┌──────────────────────┐  ┌──────────────────────────┐
│   Ollama LLM         │  │   Google Gemini API      │
│                      │  │                          │
│   Model:             │  │   Model:                 │
│   llama3.2:1b        │  │   gemini-2.0-flash-exp   │
│                      │  │                          │
│   Task:              │  │   Task:                  │
│   Extract part names │  │   Find affordable        │
│   and quantities     │  │   seller links           │
└──────────────────────┘  └──────────────────────────┘
```

## Data Flow Diagram

```
1. FILE UPLOAD
   User → Frontend → File Selection
                  ↓
2. PREVIEW (Client-side)
   Frontend (XLSX.js) → Parse CSV/Excel → Display Table
                  ↓
3. PROCESS BOM (User clicks "Find Sellers")
   Frontend → POST /api/process-bom → Backend
                  ↓
4. PARSE BOM
   Backend → csv_parser.py → Ollama API
                  ↓
         Response: [{"name": "Arduino", "quantity": 5}, ...]
                  ↓
5. GET SELLERS
   Backend → gemini_seller.py → Google Gemini API
                  ↓
         Response: [{"name": "Arduino", "sellers": [...]}]
                  ↓
6. DISPLAY RESULTS
   Backend → JSON Response → Frontend → SellerResults Component
                  ↓
         User sees table with clickable seller links
```

## Component Interaction

```
Frontend Components:
┌────────────────────────────────────────────────────────┐
│                    Index.tsx                           │
│                    (Main Page)                         │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │            FileUpload Component               │    │
│  │  • Drag & drop support                        │    │
│  │  • File validation                            │    │
│  │  • Clear button                               │    │
│  └────────────────┬──────────────────────────────┘    │
│                   │ onFileSelect                      │
│                   ▼                                   │
│  ┌──────────────────────────────────────────────┐    │
│  │           BOMPreview Component                │    │
│  │  • Table display                              │    │
│  │  • Responsive design                          │    │
│  └───────────────────────────────────────────────┘    │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │        "Find Sellers" Button                  │    │
│  │  • Loading state                              │    │
│  │  • Disabled when processing                   │    │
│  └────────────────┬──────────────────────────────┘    │
│                   │ onClick → handleProcessBOM()      │
│                   │ calls apiClient.processBOM()      │
│                   ▼                                   │
│  ┌──────────────────────────────────────────────┐    │
│  │        SellerResults Component                │    │
│  │  • Expandable cards per item                  │    │
│  │  • Seller table with links                    │    │
│  │  • External link icons                        │    │
│  └───────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────┘
```

## API Request/Response Flow

```
POST /api/process-bom
═══════════════════════════════════════

REQUEST:
┌─────────────────────────────────────┐
│  Content-Type: multipart/form-data  │
│                                     │
│  file: [Binary File Data]           │
│  └─ test_parts.csv                  │
└─────────────────────────────────────┘

BACKEND PROCESSING:
┌─────────────────────────────────────┐
│ 1. Save file temporarily            │
│ 2. csv_parser.process_csv()         │
│    └─ For each row:                 │
│       └─ query_ollama()             │
│          └─ Extract name & qty      │
│                                     │
│ 3. gemini_seller.get_seller_info()  │
│    └─ For each item:                │
│       └─ prompt_gemini()            │
│          └─ Find top 5 sellers      │
│                                     │
│ 4. Clean up temp file               │
│ 5. Return JSON response             │
└─────────────────────────────────────┘

RESPONSE:
┌─────────────────────────────────────┐
│  {                                  │
│    "success": true,                 │
│    "parsed_data": [                 │
│      {                              │
│        "name": "Arduino Uno",       │
│        "quantity": 5                │
│      }                              │
│    ],                               │
│    "seller_info": [                 │
│      {                              │
│        "name": "Arduino Uno",       │
│        "quantity": 5,               │
│        "sellers": [                 │
│          {                          │
│            "company": "Adafruit",   │
│            "link": "https://..."    │
│          }                          │
│        ]                            │
│      }                              │
│    ]                                │
│  }                                  │
└─────────────────────────────────────┘
```

## File Type Support Flow

```
USER UPLOADS FILE
       │
       ├── .csv / .txt
       │   └─→ Frontend: Parse with text split
       │       Backend: pandas.read_csv()
       │
       ├── .xlsx / .xls
       │   └─→ Frontend: Parse with XLSX.js
       │       Backend: pandas.read_csv() with openpyxl
       │
       └── Other formats
           └─→ Rejected with error message
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────┐
│              Error Scenarios                    │
└─────────────────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Frontend │   │ Backend  │   │ External │
│  Errors  │   │  Errors  │   │ API Errors│
└─────┬────┘   └────┬─────┘   └────┬─────┘
      │             │              │
      │             │              │
      ▼             ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│• No file │   │• Invalid │   │• Ollama  │
│  selected│   │  file    │   │  down    │
│• Invalid │   │  format  │   │• Gemini  │
│  format  │   │• Parsing │   │  API     │
│• Network │   │  failed  │   │  quota   │
│  error   │   │• Process │   │  exceeded│
└─────┬────┘   │  timeout │   └────┬─────┘
      │        └────┬─────┘        │
      │             │              │
      └─────────────┼──────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  Toast Message   │
         │  • Error title   │
         │  • Description   │
         │  • Red styling   │
         └──────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────┐
│                 FRONTEND                        │
├─────────────────────────────────────────────────┤
│  React 18         │  Component framework        │
│  TypeScript       │  Type safety                │
│  Vite             │  Build tool & dev server    │
│  Tailwind CSS     │  Styling                    │
│  shadcn/ui        │  UI components              │
│  React Query      │  State management           │
│  XLSX.js          │  Excel parsing              │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                 BACKEND                         │
├─────────────────────────────────────────────────┤
│  Flask            │  Web framework              │
│  Flask-CORS       │  Cross-origin support       │
│  pandas           │  Data processing            │
│  openpyxl         │  Excel file support         │
│  Werkzeug         │  File upload handling       │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│               AI/ML SERVICES                    │
├─────────────────────────────────────────────────┤
│  Ollama           │  Local LLM inference        │
│  llama3.2:1b      │  Part extraction model      │
│  Google Gemini    │  Seller recommendation      │
│  gemini-2.0       │  Advanced reasoning         │
└─────────────────────────────────────────────────┘
```

## Deployment Architecture (Production)

```
┌────────────────────────────────────────────────┐
│              Cloud Provider                    │
│                                                │
│  ┌──────────────────────────────────────┐    │
│  │  Frontend (Vercel/Netlify)            │    │
│  │  • Static site hosting                │    │
│  │  • CDN distribution                   │    │
│  │  • HTTPS enabled                      │    │
│  └───────────────┬──────────────────────┘    │
│                  │                            │
│                  │ HTTPS/API                  │
│                  ▼                            │
│  ┌──────────────────────────────────────┐    │
│  │  Backend (Railway/Heroku)             │    │
│  │  • Python runtime                     │    │
│  │  • Gunicorn WSGI server               │    │
│  │  • Environment variables              │    │
│  └───────────────┬──────────────────────┘    │
│                  │                            │
│         ┌────────┴────────┐                  │
│         ▼                 ▼                  │
│  ┌─────────────┐   ┌─────────────┐          │
│  │ Ollama      │   │  Gemini API │          │
│  │ (Self-host) │   │  (Google)   │          │
│  └─────────────┘   └─────────────┘          │
└────────────────────────────────────────────────┘
```
