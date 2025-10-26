#!/bin/bash
# Example script to run Claude browser automation on the example BOM

echo "🚀 Claude Browser Automation - Example Run"
echo ""
echo "This script will:"
echo "  1. Use Claude AI to intelligently search for parts"
echo "  2. Open a browser and navigate to the specified website"
echo "  3. Search for each part in example_bom.csv"
echo "  4. Extract prices and product information"
echo "  5. Attempt to add items to cart"
echo ""
echo "⚠️  Requirements:"
echo "  - ANTHROPIC_API_KEY environment variable must be set"
echo "  - Browser will be visible (recommended for Cloudflare-protected sites)"
echo ""

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY environment variable is not set"
    echo ""
    echo "To fix this, run:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    exit 1
fi

# Default website
WEBSITE=${1:-"https://www.adafruit.com"}

echo "📋 Using BOM file: example_bom.csv"
echo "🌐 Searching on: $WEBSITE"
echo ""
echo "Press Enter to continue, or Ctrl+C to cancel..."
read

# Run the automation
python3 claude_browser_automation.py \
    example_bom.csv \
    --website "$WEBSITE" \
    --output "claude_results.json"

echo ""
echo "✅ Done! Check claude_results.json for detailed results."

