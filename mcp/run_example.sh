#!/bin/bash

# example script showing how to run with open source models

echo "=========================================="
echo "BOM Ordering with Open Source Models"
echo "=========================================="
echo ""

# check if ollama is running
echo "checking if ollama is running..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ ollama is running"
else
    echo "✗ ollama is not running"
    echo "  start it with: ollama serve"
    echo "  then run this script again"
    exit 1
fi

# check if llama3.1 is installed
echo "checking if llama3.1 is installed..."
if ollama list | grep -q "llama3.1"; then
    echo "✓ llama3.1 is installed"
else
    echo "✗ llama3.1 not found"
    echo "  installing llama3.1..."
    ollama pull llama3.1
fi

echo ""
echo "=========================================="
echo "running bom ordering system..."
echo "=========================================="
echo ""

# run the system with open source model
python3 main.py example_bom.csv \
    --use-open-source \
    --model-name llama3.1 \
    --base-url http://localhost:11434/v1 \
    --num-websites 3 \
    --output example_results.csv

echo ""
echo "=========================================="
echo "done! check example_results.csv"
echo "=========================================="


