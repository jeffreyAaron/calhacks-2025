# User Journey Guide

## The Complete User Experience

### Step 1: Starting the Application

```
Terminal:
┌─────────────────────────────────────────────────┐
│ $ ./start.sh                                    │
│                                                 │
│ 🚀 Starting BOM to Order Application           │
│                                                 │
│ 🐍 Starting Backend Server (Flask)...          │
│ ✅ Backend running on http://localhost:5000    │
│                                                 │
│ ⚛️  Starting Frontend Server (Vite)...         │
│ ✅ Frontend running on http://localhost:5173   │
│                                                 │
│ Press Ctrl+C to stop all servers                │
└─────────────────────────────────────────────────┘
```

### Step 2: Opening the Application

```
Browser → http://localhost:5173
┌────────────────────────────────────────────────────────────┐
│  [📦] BOM Upload Portal                                    │
│  ────────────────────────────────────────────────────────  │
│       Upload and preview your Bill of Materials files      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                                                       │ │
│  │    [📁]  Drag & drop your BOM file here             │ │
│  │           or click to browse                         │ │
│  │                                                       │ │
│  │    Supported: CSV, Excel (XLSX, XLS), Text files    │ │
│  │                                                       │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                   │
│  │   📄    │  │   👁️    │  │   🔒    │                   │
│  │Multiple │  │ Instant  │  │Client-  │                   │
│  │Formats  │  │ Preview  │  │Side Only│                   │
│  └─────────┘  └─────────┘  └─────────┘                   │
└────────────────────────────────────────────────────────────┘
```

### Step 3: Uploading a File

```
User drags test_parts.csv onto the upload area
        ↓
┌────────────────────────────────────────────────────────────┐
│  [📦] BOM Upload Portal                                    │
│  ────────────────────────────────────────────────────────  │
│                                                             │
│  ✅ File Selected: test_parts.csv (1.2 KB)                │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  📊 BOM Preview                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Part Name          │ Quantity                        │ │
│  ├──────────────────────────────────────────────────────┤ │
│  │ Raspberry Pi 4     │ 2                               │ │
│  │ Arduino Uno        │ 5                               │ │
│  │ Breadboard         │ 10                              │ │
│  │ Jumper Wires       │ 50                              │ │
│  │ USB-C Cable        │ 3                               │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│               [  Find Sellers  ]                            │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Step 4: Processing (User Clicks "Find Sellers")

```
┌────────────────────────────────────────────────────────────┐
│                                                             │
│  📊 BOM Preview                                             │
│  [Table showing 5 items...]                                 │
│                                                             │
│               [⏳ Processing...  ]  ← Button disabled      │
│                                                             │
│  ┌────────────────────────────────────────────────┐       │
│  │  🔄 Analyzing BOM with AI...                   │       │
│  │     • Extracting part names                    │       │
│  │     • Finding quantities                       │       │
│  │     • Searching for sellers                    │       │
│  └────────────────────────────────────────────────┘       │
└────────────────────────────────────────────────────────────┘

Backend Processing:
┌──────────────────────────────────┐
│ Step 1: Parse with Ollama        │
│ [████████████░░░░░░░░] 60%      │
│                                  │
│ Step 2: Query Gemini for sellers│
│ [██████████████████░░] 90%      │
└──────────────────────────────────┘
```

### Step 5: Results Display

```
┌────────────────────────────────────────────────────────────┐
│  📊 BOM Preview                                             │
│  [Table showing parsed items...]                            │
│                                                             │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  📦 Seller Recommendations                                  │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Raspberry Pi 4                    Quantity: 2        │ │
│  │ ────────────────────────────────────────────────────  │ │
│  │  Seller          │ Link                              │ │
│  │  ────────────────────────────────────────────────    │ │
│  │  Adafruit        │ 🔗 Visit Site                     │ │
│  │  SparkFun        │ 🔗 Visit Site                     │ │
│  │  Pololu          │ 🔗 Visit Site                     │ │
│  │  Amazon          │ 🔗 Visit Site                     │ │
│  │  Mouser          │ 🔗 Visit Site                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Arduino Uno                       Quantity: 5        │ │
│  │ ────────────────────────────────────────────────────  │ │
│  │  Seller          │ Link                              │ │
│  │  ────────────────────────────────────────────────    │ │
│  │  Arduino.cc      │ 🔗 Visit Site                     │ │
│  │  Adafruit        │ 🔗 Visit Site                     │ │
│  │  SparkFun        │ 🔗 Visit Site                     │ │
│  │  Amazon          │ 🔗 Visit Site                     │ │
│  │  AliExpress      │ 🔗 Visit Site                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  [Similar cards for other items...]                        │
│                                                             │
└────────────────────────────────────────────────────────────┘

✅ Toast Notification (top-right corner):
┌────────────────────────────────┐
│ Processing complete!           │
│ Found seller information for   │
│ 5 items                        │
└────────────────────────────────┘
```

### Step 6: Exploring Results

```
User clicks "Visit Site" on Adafruit for Raspberry Pi 4
        ↓
New browser tab opens → https://www.adafruit.com
┌────────────────────────────────────────────────────────────┐
│  🌐 Adafruit Industries                                    │
│  [Adafruit's product page opens]                           │
└────────────────────────────────────────────────────────────┘

Original tab remains open with all results still visible
```

## Error Scenarios

### Scenario 1: No File Selected

```
User clicks "Find Sellers" without uploading
        ↓
❌ Toast Notification:
┌────────────────────────────────┐
│ No file selected               │
│ Please select a BOM file first │
└────────────────────────────────┘
```

### Scenario 2: Invalid File Type

```
User uploads file.pdf
        ↓
❌ Toast Notification:
┌────────────────────────────────┐
│ Invalid file type              │
│ Only CSV, TXT, XLSX, XLS       │
│ files allowed                  │
└────────────────────────────────┘
```

### Scenario 3: Backend Not Running

```
User clicks "Find Sellers" but backend is down
        ↓
❌ Toast Notification:
┌────────────────────────────────┐
│ Processing failed              │
│ Cannot connect to server       │
└────────────────────────────────┘

Browser Console (F12):
┌────────────────────────────────┐
│ ❌ POST http://localhost:5000  │
│    /api/process-bom            │
│    net::ERR_CONNECTION_REFUSED │
└────────────────────────────────┘
```

### Scenario 4: Ollama Not Available

```
Backend receives request but Ollama is not running
        ↓
Backend Terminal:
┌────────────────────────────────┐
│ Error: [Errno 2] No such file  │
│ or directory: 'ollama'         │
└────────────────────────────────┘

User sees:
❌ Toast Notification:
┌────────────────────────────────┐
│ Processing failed              │
│ LLM service unavailable        │
└────────────────────────────────┘
```

## Success Flow Summary

```
1. START
   │
   ├─→ User runs ./start.sh
   │   ✅ Both servers start
   │
2. UPLOAD
   │
   ├─→ User visits http://localhost:5173
   ├─→ User uploads BOM file
   │   ✅ File preview appears
   │
3. PROCESS
   │
   ├─→ User clicks "Find Sellers"
   ├─→ Frontend sends file to backend
   ├─→ Backend parses with Ollama
   ├─→ Backend queries Gemini
   │   ✅ Processing complete notification
   │
4. RESULTS
   │
   ├─→ Seller cards appear on page
   ├─→ Each item shows 5 seller options
   │   ✅ All links are clickable
   │
5. EXPLORE
   │
   ├─→ User clicks seller links
   │   ✅ Seller websites open in new tabs
   │
6. REPEAT
   │
   └─→ User can upload another file
       ✅ Previous results are cleared
```

## Time Expectations

```
┌─────────────────────────────┬──────────────┐
│ Action                      │ Time         │
├─────────────────────────────┼──────────────┤
│ Starting servers            │ 3-5 seconds  │
│ Frontend page load          │ < 1 second   │
│ File upload & preview       │ Instant      │
│ Parsing with Ollama         │ 2-5 seconds  │
│ Querying Gemini (5 items)   │ 10-15 seconds│
│ Total processing (5 items)  │ 15-20 seconds│
│ Displaying results          │ Instant      │
└─────────────────────────────┴──────────────┘

* Times may vary based on:
  - File size
  - Number of items
  - Internet speed (for Gemini)
  - Computer performance (for Ollama)
```

## What Users See vs. What Happens Behind the Scenes

```
USER VIEW                          BEHIND THE SCENES
═════════════════════════════════════════════════════════

[Upload File]                    → File stored in memory
                                   XLSX.js parses locally
                                   
[Preview Table]                  → Data rendered from 
                                   parsed array
                                   
[Click "Find Sellers"]           → POST /api/process-bom
                                   File sent to backend
                                   
[Loading Indicator]              → Backend processing:
                                   1. Save temp file
                                   2. Call csv_parser.py
                                   3. Ollama extracts data
                                   4. Call gemini_seller.py
                                   5. Gemini finds sellers
                                   6. Delete temp file
                                   7. Return JSON
                                   
[Results Appear]                 → Frontend receives JSON
                                   SellerResults component
                                   renders data
                                   
[Click Seller Link]              → window.open(url, '_blank')
                                   New tab opens
```

## Mobile Experience

```
On smaller screens:
┌────────────────────┐
│ [📦] BOM Upload    │
│ ─────────────────  │
│                    │
│ [📁] Upload Area   │
│  (full width)      │
│                    │
│ ──────────────────│
│                    │
│ 📊 BOM Preview     │
│ ┌────────────────┐│
│ │ Part | Qty     ││
│ ├────────────────┤│
│ │ [Scroll table] ││
│ └────────────────┘│
│                    │
│ [ Find Sellers ]   │
│  (full width)      │
│                    │
│ 📦 Seller Results  │
│ ┌────────────────┐│
│ │ [Cards stack]  ││
│ │ vertically     ││
│ └────────────────┘│
└────────────────────┘
```

---

This completes the user journey! The system is designed to be intuitive and provide clear feedback at every step.
