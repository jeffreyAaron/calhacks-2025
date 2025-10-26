#!/bin/bash
# Quick start script for Claude + Browser MCP

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║          🚀 Claude + Browser MCP Quick Start                  ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY environment variable is not set"
    echo ""
    echo "To fix this, run:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    echo "Get your API key at: https://console.anthropic.com/"
    exit 1
fi

echo "✅ ANTHROPIC_API_KEY is set"
echo ""

# Check if Python packages are installed
echo "🔍 Checking Python packages..."
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo "⚠️  anthropic package not found. Installing..."
    pip install -r requirements.txt
else
    echo "✅ Python packages installed"
fi

echo ""

# Run test script
echo "🧪 Testing setup..."
python3 test_browser_mcp.py

# Check test result
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                     ✅ Setup Complete!                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Ready to run! Try:"
    echo ""
    echo "  python3 claude_with_browser_mcp.py example_bom.csv"
    echo ""
    echo "Or with custom website:"
    echo ""
    echo "  python3 claude_with_browser_mcp.py example_bom.csv \\"
    echo "      --website https://www.sparkfun.com"
    echo ""
else
    echo ""
    echo "❌ Setup test failed. Please fix the issues above."
    exit 1
fi

