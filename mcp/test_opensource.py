#!/usr/bin/env python3

from browser_controller import BrowserController

def test_ollama_connection():
    # test if ollama is running and accessible
    print("testing ollama connection with llama3.1...")
    print("=" * 50)
    
    try:
        # initialize controller with open source settings
        controller = BrowserController(
            use_open_source=True,
            model_name="llama3.1",
            base_url="http://localhost:11434/v1"
        )
        
        print("✓ browser controller initialized")
        print(f"✓ using model: {controller.model_name}")
        print(f"✓ base url: {controller.base_url}")
        print("\ntesting llm response...")
        
        # simple test - search for a part
        result = controller.search_part_on_website(
            part_name="Arduino Uno R3",
            website_url="https://www.digikey.com"
        )
        
        print("\nresult from llm:")
        print(f"  product_name: {result.get('product_name')}")
        print(f"  product_url: {result.get('product_url')}")
        print(f"  price: {result.get('price')}")
        
        if result.get('product_url'):
            print("\n✓ open source model is working!")
        else:
            print("\n⚠ model responded but no product found (this is normal without full mcp)")
            
        print("\nnote: full functionality requires mcp server for browser automation")
        
    except Exception as e:
        print(f"\n✗ error: {e}")
        print("\ntroubleshooting:")
        print("1. ensure ollama is running: ollama serve")
        print("2. ensure model is installed: ollama pull llama3.1")
        print("3. test ollama: curl http://localhost:11434/api/tags")


def test_lm_studio_connection():
    # test lm studio connection
    print("\n\ntesting lm studio connection...")
    print("=" * 50)
    
    try:
        controller = BrowserController(
            use_open_source=True,
            model_name="llama-3.1-8b-instruct",
            base_url="http://localhost:1234/v1"
        )
        
        print("✓ browser controller initialized")
        print(f"✓ using model: {controller.model_name}")
        print(f"✓ base url: {controller.base_url}")
        print("\nif lm studio is running, this should work!")
        
    except Exception as e:
        print(f"\n✗ error: {e}")
        print("\ntroubleshooting:")
        print("1. ensure lm studio is running")
        print("2. ensure server is started in lm studio")
        print("3. check the port (default: 1234)")


if __name__ == "__main__":
    print("open source model connection test")
    print("=" * 50)
    print()
    
    # test ollama first
    test_ollama_connection()
    
    # optionally test lm studio
    print("\n\nwant to test lm studio? (y/n): ", end="")
    try:
        response = input().strip().lower()
        if response == 'y':
            test_lm_studio_connection()
    except:
        pass
    
    print("\n\ndone!")


