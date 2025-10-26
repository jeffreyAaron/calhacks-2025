"""
Test script to verify Browser MCP connection
This tests that you can connect to the Browser MCP Chrome extension
"""
import os
import sys


def check_environment():
    """Check if environment is set up correctly"""
    print("🔍 Checking environment setup...\n")
    
    issues = []
    
    # Check for Anthropic API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        print("✅ ANTHROPIC_API_KEY is set")
    else:
        print("❌ ANTHROPIC_API_KEY is not set")
        issues.append("Set ANTHROPIC_API_KEY: export ANTHROPIC_API_KEY='your-key'")
    
    # Check for mcp.json
    mcp_config = os.path.expanduser("~/.cursor/mcp.json")
    if os.path.exists(mcp_config):
        print(f"✅ MCP config found at {mcp_config}")
        try:
            import json
            with open(mcp_config, 'r') as f:
                config = json.load(f)
                if 'mcpServers' in config and 'browsermcp' in config['mcpServers']:
                    print("✅ Browser MCP server is configured")
                else:
                    print("❌ Browser MCP server not found in config")
                    issues.append("Add browsermcp to ~/.cursor/mcp.json")
        except Exception as e:
            print(f"⚠️  Could not parse mcp.json: {e}")
    else:
        print(f"❌ MCP config not found at {mcp_config}")
        issues.append(f"Create MCP config at {mcp_config}")
    
    # Check for required Python packages
    print("\n🔍 Checking Python packages...")
    
    required_packages = {
        'anthropic': 'Anthropic API client',
    }
    
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} is installed ({description})")
        except ImportError:
            print(f"❌ {package} is not installed ({description})")
            issues.append(f"Install {package}: pip install {package}")
    
    # Check for example BOM file
    print("\n🔍 Checking for example files...")
    if os.path.exists('example_bom.csv'):
        print("✅ example_bom.csv found")
    else:
        print("⚠️  example_bom.csv not found (optional)")
    
    # Print summary
    print("\n" + "="*70)
    if issues:
        print("❌ SETUP INCOMPLETE - Issues found:\n")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        print("\n" + "="*70)
        return False
    else:
        print("✅ ALL CHECKS PASSED - Ready to use!")
        print("="*70)
        return True


def test_claude_connection():
    """Test connection to Claude API"""
    print("\n🧪 Testing Claude API connection...")
    
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ Cannot test: ANTHROPIC_API_KEY not set")
            return False
        
        client = Anthropic(api_key=api_key)
        
        # Make a simple API call
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Say 'Hello from Claude!'"
            }]
        )
        
        message = response.content[0].text
        print(f"✅ Claude responded: {message}")
        return True
        
    except Exception as e:
        print(f"❌ Claude API test failed: {e}")
        return False


def show_next_steps():
    """Show user what to do next"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                      🎉 READY TO GO!                          ║
╚════════════════════════════════════════════════════════════════╝

To use Claude with Browser MCP:

1. Make sure Chrome is open with the Browser MCP extension installed

2. Run the automation:
   
   python claude_with_browser_mcp.py example_bom.csv \\
       --website https://www.adafruit.com

3. Watch as Claude:
   • Opens the website in your browser
   • Searches for each part in the BOM
   • Finds prices and product information
   • Adds items to your cart

📚 For more options, run:
   python claude_with_browser_mcp.py --help

📝 To test with your own BOM:
   python claude_with_browser_mcp.py your_bom.csv \\
       --website https://www.sparkfun.com \\
       --output results.json

═══════════════════════════════════════════════════════════════
    """)


def main():
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║           🧪 Browser MCP Setup Test                           ║
║                                                                ║
║  This script checks if your environment is properly           ║
║  configured to use Claude with Browser MCP                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Check environment
    env_ok = check_environment()
    
    if not env_ok:
        print("\n⚠️  Please fix the issues above before continuing.")
        return 1
    
    # Test Claude connection
    claude_ok = test_claude_connection()
    
    if not claude_ok:
        print("\n⚠️  Claude API connection failed. Check your API key.")
        return 1
    
    # Show next steps
    show_next_steps()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

