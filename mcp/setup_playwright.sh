#!/bin/bash

echo "=========================================="
echo "Setting up Playwright for Browser Automation"
echo "=========================================="
echo ""

# install python dependencies
echo "installing python dependencies..."
pip install playwright

# install playwright browsers
echo ""
echo "installing playwright browsers (chromium, firefox, webkit)..."
playwright install chromium

echo ""
echo "=========================================="
echo "✓ playwright setup complete!"
echo "=========================================="
echo ""
echo "you can now run:"
echo "  python main.py example_bom.csv --show-browser    # see browser window"
echo "  python main.py example_bom.csv --headless        # run in background"


