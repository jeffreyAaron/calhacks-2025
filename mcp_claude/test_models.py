#!/usr/bin/env python3
"""
Quick test script to find which Claude models are available with your API key
"""
import os
from anthropic import Anthropic

# Models to try
MODELS_TO_TEST = [
    "claude-3-5-sonnet-latest",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-latest",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

def test_model(client, model_name):
    """Test if a model is available"""
    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        return True, response.content[0].text
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("🔍 Testing which Claude models are available with your API key")
    print("=" * 70)
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n❌ ANTHROPIC_API_KEY not set!")
        print("Run: export ANTHROPIC_API_KEY='your-key'")
        return 1
    
    print(f"\n✅ API Key found: {api_key[:15]}...{api_key[-4:]}")
    print(f"\n{'Model':<35} {'Status':<15} {'Response'}")
    print("-" * 70)
    
    client = Anthropic(api_key=api_key)
    available_models = []
    
    for model in MODELS_TO_TEST:
        success, response = test_model(client, model)
        
        if success:
            status = "✅ AVAILABLE"
            available_models.append(model)
            response_preview = response[:30] if response else ""
        else:
            status = "❌ NOT FOUND"
            response_preview = ""
        
        print(f"{model:<35} {status:<15} {response_preview}")
    
    print("\n" + "=" * 70)
    if available_models:
        print(f"✅ Found {len(available_models)} available model(s):")
        for model in available_models:
            print(f"   • {model}")
        print(f"\nRecommended: {available_models[0]}")
    else:
        print("❌ No models found! Check your API key.")
    print("=" * 70)
    
    return 0 if available_models else 1

if __name__ == '__main__':
    exit(main())

