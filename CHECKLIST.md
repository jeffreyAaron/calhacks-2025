# Setup Checklist

Use this checklist to ensure everything is configured correctly.

## ✅ Prerequisites

- [ ] Python 3.8 or higher installed
  ```bash
  python --version
  ```

- [ ] Node.js 18 or higher installed
  ```bash
  node --version
  ```

- [ ] pnpm installed (or npm)
  ```bash
  pnpm --version
  ```

- [ ] Ollama installed
  ```bash
  ollama --version
  ```

- [ ] Git installed (for version control)
  ```bash
  git --version
  ```

## ✅ Ollama Setup

- [ ] Ollama is installed from https://ollama.ai

- [ ] llama3.2:1b model is pulled
  ```bash
  ollama pull llama3.2:1b
  ```

- [ ] Verify model is available
  ```bash
  ollama list
  # Should show llama3.2:1b in the list
  ```

- [ ] Test Ollama is working
  ```bash
  ollama run llama3.2:1b "Hello"
  ```

## ✅ Google Gemini API

- [ ] Have a Google Cloud account

- [ ] Created a Gemini API key from https://makersuite.google.com/app/apikey

- [ ] Created `API_Key.txt` file in project root
  ```bash
  echo "your-api-key-here" > API_Key.txt
  ```

- [ ] Verify file exists and has content
  ```bash
  cat API_Key.txt
  ```

## ✅ Backend Setup

- [ ] Navigate to backend directory
  ```bash
  cd backend
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify all packages installed successfully
  ```bash
  python -c "import flask, pandas, google.generativeai; print('✅ All packages installed')"
  ```

- [ ] Return to project root
  ```bash
  cd ..
  ```

## ✅ Frontend Setup

- [ ] Navigate to frontend directory
  ```bash
  cd "BOM to Order/frontend"
  ```

- [ ] Install Node dependencies
  ```bash
  pnpm install
  ```

- [ ] Verify `.env` file exists with correct URL
  ```bash
  cat .env
  # Should show: VITE_API_URL=http://localhost:5000
  ```

- [ ] Return to project root
  ```bash
  cd ../..
  ```

## ✅ File Verification

- [ ] Verify all key files exist:
  ```bash
  ls -1 backend/app.py \
        backend/csv_parser.py \
        backend/gemini_seller.py \
        backend/requirements.txt \
        "BOM to Order/frontend/src/lib/api.ts" \
        "BOM to Order/frontend/src/components/SellerResults.tsx" \
        API_Key.txt
  ```

- [ ] Test file exists for testing
  ```bash
  ls -1 test_parts.csv
  ```

## ✅ First Run

- [ ] Make start script executable
  ```bash
  chmod +x start.sh
  ```

- [ ] Start both servers
  ```bash
  ./start.sh
  # OR
  python start.py
  ```

- [ ] Verify backend is running
  ```bash
  # In a new terminal
  curl http://localhost:5000/health
  # Should return: {"status":"healthy"}
  ```

- [ ] Verify frontend is accessible
  - Open browser to http://localhost:5173
  - Should see "BOM Upload Portal" page

## ✅ Integration Test

- [ ] Backend health check passes
  ```bash
  python test_backend.py
  ```

- [ ] Frontend loads without errors
  - Check browser console (F12) - no red errors

- [ ] Can upload a file
  - Drag & drop test_parts.csv
  - Should see preview table

- [ ] Can process BOM
  - Click "Find Sellers" button
  - Should show loading indicator
  - Should display seller results after processing

- [ ] Seller links are clickable
  - Click on any seller link
  - Should open in new tab

## ✅ Manual Testing

- [ ] Test with CSV file
  - Upload test_parts.csv
  - Verify data displays correctly

- [ ] Test with Excel file (if available)
  - Upload .xlsx or .xls file
  - Verify data displays correctly

- [ ] Test error handling
  - Try uploading invalid file type
  - Should show error message

- [ ] Test with backend stopped
  - Stop backend server
  - Try processing BOM
  - Should show error toast

## ✅ Optional Configuration

- [ ] Configure VS Code Python environment
  ```bash
  # In VS Code, select Python interpreter
  # Cmd+Shift+P → "Python: Select Interpreter"
  ```

- [ ] Set up version control (if not already)
  ```bash
  git add .
  git commit -m "Connected frontend to backend"
  ```

- [ ] Create production environment file
  ```bash
  cp "BOM to Order/frontend/.env" "BOM to Order/frontend/.env.production"
  # Edit .env.production with production API URL
  ```

## ✅ Documentation Review

- [ ] Read [README.md](README.md) - Project overview
- [ ] Read [SETUP.md](SETUP.md) - Detailed setup guide  
- [ ] Read [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [ ] Read [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md) - Integration details
- [ ] Read [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [ ] Read [backend/README.md](backend/README.md) - API documentation

## ✅ Troubleshooting Checks

If something isn't working, verify:

- [ ] No other process is using port 5000
  ```bash
  lsof -i :5000
  ```

- [ ] No other process is using port 5173
  ```bash
  lsof -i :5173
  ```

- [ ] All dependencies are installed
  ```bash
  pip list | grep -E "flask|pandas|google"
  ```

- [ ] Environment variables are set
  ```bash
  cat "BOM to Order/frontend/.env"
  ```

- [ ] API key file exists and is readable
  ```bash
  test -r API_Key.txt && echo "✅ File is readable"
  ```

- [ ] Ollama service is running
  ```bash
  ollama list
  ```

## 🎉 Success Indicators

You'll know everything is working when:

✅ Both servers start without errors
✅ Can access frontend at http://localhost:5173
✅ Can access backend health check at http://localhost:5000/health
✅ Can upload and preview BOM files
✅ "Find Sellers" button works and shows results
✅ Seller links are clickable and valid
✅ No errors in browser console or terminal

## 📞 Getting Help

If you're stuck:

1. Check the [SETUP.md](SETUP.md#troubleshooting) troubleshooting section
2. Run `python test_backend.py` to diagnose backend issues
3. Check browser console (F12) for frontend errors
4. Check terminal output for backend errors
5. Verify all items in this checklist are complete

---

**Once all items are checked, you're ready to go!** 🚀

Start the application with:
```bash
./start.sh
```

Then visit http://localhost:5173 and start processing BOM files!
