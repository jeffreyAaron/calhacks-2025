# Quick Reference Guide

## Starting the Application

### Automated (Easiest)
```bash
./start.sh
# or
python start.py
```

### Manual
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend  
cd "BOM to Order/frontend"
pnpm dev
```

## URLs
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## File Flow

1. **Upload** → File sent to frontend
2. **Preview** → Parsed client-side by XLSX.js
3. **Process** → File sent to backend via `/api/process-bom`
4. **Parse** → Ollama extracts parts & quantities
5. **Lookup** → Gemini finds sellers
6. **Display** → Results shown in UI

## Common Commands

### Backend
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run server
cd backend && python app.py

# Test endpoint
curl http://localhost:5000/health
```

### Frontend
```bash
# Install dependencies
cd "BOM to Order/frontend"
pnpm install

# Run dev server
pnpm dev

# Build for production
pnpm build
```

### Ollama
```bash
# Pull model
ollama pull llama3.2:1b

# List models
ollama list

# Test model
ollama run llama3.2:1b "Hello"
```

## API Examples

### Parse BOM
```bash
curl -X POST http://localhost:5000/api/parse-bom \
  -F "file=@test_parts.csv"
```

### Get Sellers
```bash
curl -X POST http://localhost:5000/api/get-sellers \
  -H "Content-Type: application/json" \
  -d '{"items": [{"name": "Arduino Uno", "quantity": 5}]}'
```

### Complete Pipeline
```bash
curl -X POST http://localhost:5000/api/process-bom \
  -F "file=@test_parts.csv"
```

## Environment Variables

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:5000
```

### Backend (API_Key.txt)
```bash
echo "your-gemini-api-key" > API_Key.txt
```

## Troubleshooting Quick Fixes

### Backend won't start
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r backend/requirements.txt

# Check if port is in use
lsof -i :5000
```

### Frontend won't start
```bash
# Clean install
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Check Node version (need 18+)
node --version
```

### Ollama issues
```bash
# Check if running
ollama list

# Restart Ollama
# macOS: Restart from menu bar
# Linux: systemctl restart ollama
```

### CORS errors
- Ensure backend is running first
- Check VITE_API_URL in frontend/.env
- Verify CORS is enabled in backend/app.py

## File Types Supported

- **CSV**: `.csv`, `.txt`
- **Excel**: `.xlsx`, `.xls`
- **Max Size**: 16MB

## Development Workflow

1. Make changes to backend → Automatically reloads (Flask debug mode)
2. Make changes to frontend → Hot module replacement (Vite HMR)
3. Test locally before committing
4. API changes require frontend type updates in `lib/api.ts`

## Production Checklist

- [ ] Build frontend: `pnpm run build`
- [ ] Use production WSGI server: `gunicorn`
- [ ] Set production API URL in frontend
- [ ] Move API key to environment variable
- [ ] Configure CORS for production domain
- [ ] Enable HTTPS
- [ ] Set up error logging
- [ ] Configure rate limiting

## Key Files to Know

| File                                        | Purpose                     |
| ------------------------------------------- | --------------------------- |
| `backend/app.py`                            | Flask API server & routes   |
| `backend/csv_parser.py`                     | Ollama BOM parsing logic    |
| `backend/gemini_seller.py`                  | Gemini seller lookup        |
| `frontend/src/lib/api.ts`                   | API client functions        |
| `frontend/src/pages/Index.tsx`              | Main page component         |
| `frontend/src/components/SellerResults.tsx` | Results display             |
| `API_Key.txt`                               | Gemini API key (not in git) |

## Need Help?

1. Check [SETUP.md](SETUP.md) for detailed setup
2. Check [backend/README.md](backend/README.md) for API docs
3. View logs in terminal where servers are running
4. Check browser console for frontend errors
5. Check terminal for backend errors
