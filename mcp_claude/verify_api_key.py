#!/usr/bin/env python3
"""
Verify Anthropic API key is valid
"""
import os
import sys

print("=" * 70)
print("🔑 Anthropic API Key Verification")
print("=" * 70)

# Check if key exists
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    print("\n❌ ANTHROPIC_API_KEY environment variable is not set!")
    print("\nTo fix:")
    print("  export ANTHROPIC_API_KEY='your-key-here'")
    sys.exit(1)

print(f"\n✅ API Key found")
print(f"   Prefix: {api_key[:20]}...")
print(f"   Suffix: ...{api_key[-10:]}")
print(f"   Length: {len(api_key)} characters")

# Check format
if api_key.startswith('sk-ant-'):
    print("\n✅ Key format looks correct (starts with 'sk-ant-')")
elif api_key.startswith('sk-proj-') or (api_key.startswith('sk-') and not api_key.startswith('sk-ant-')):
    print("\n❌ WARNING: This looks like an OpenAI API key, not Anthropic!")
    print("   OpenAI keys start with: sk-proj- or sk-...")
    print("   Anthropic keys start with: sk-ant-")
    print("\n   Get an Anthropic key at: https://console.anthropic.com/")
    sys.exit(1)
else:
    print("\n⚠️  Warning: Unusual key format")

# Try to import anthropic
print("\n📦 Checking anthropic package...")
try:
    from anthropic import Anthropic
    print("✅ anthropic package is installed")
except ImportError:
    print("❌ anthropic package not installed!")
    print("   Run: pip install anthropic")
    sys.exit(1)

# Try a simple API call
print("\n🧪 Testing API connection...")
try:
    client = Anthropic(api_key=api_key)
    
    # Try multiple models
    models_to_try = [
        "claude-3-haiku-20240307",  # Cheapest, should be most available
        "claude-3-sonnet-20240229",
        "claude-3-opus-20240229",
        "claude-3-5-sonnet-20240620",
        "claude-3-5-sonnet-20241022",
    ]
    
    success = False
    working_model = None
    
    for model in models_to_try:
        try:
            print(f"   Trying {model}...", end=" ")
            response = client.messages.create(
                model=model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            print(f"✅ WORKS!")
            success = True
            working_model = model
            break
        except Exception as e:
            if "not_found_error" in str(e):
                print(f"❌ Not found")
            elif "authentication_error" in str(e):
                print(f"❌ Auth error - invalid key?")
                break
            else:
                print(f"❌ {str(e)[:50]}")
    
    if success:
        print(f"\n🎉 SUCCESS! Your API key works!")
        print(f"   Working model: {working_model}")
        print(f"\nYou can use this model in the scripts.")
    else:
        print(f"\n❌ FAILED: No models accessible with this key")
        print(f"\nPossible issues:")
        print(f"   1. API key is invalid or expired")
        print(f"   2. API key doesn't have access to any models")
        print(f"   3. Account needs to be activated")
        print(f"\n   Check your account at: https://console.anthropic.com/")

except Exception as e:
    print(f"❌ API Error: {e}")
    print(f"\nThis usually means:")
    print(f"   1. Invalid API key")
    print(f"   2. Network connection issue")
    print(f"   3. API endpoint unavailable")

print("\n" + "=" * 70)

