#!/usr/bin/env python3
"""
Test script to verify backend is working correctly
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_parse_bom():
    """Test BOM parsing with a sample file"""
    print("\n📝 Testing BOM parsing...")
    
    # Create a simple test CSV
    test_csv = "part_name,qty\nArduino Uno,5\nRaspberry Pi 4,2"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/parse-bom",
            files={"file": ("test.csv", test_csv, "text/csv")}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Parse BOM passed")
            print(f"   Parsed {len(data['data'])} items")
            return True
        else:
            print(f"❌ Parse BOM failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Parse BOM error: {e}")
        return False

def test_get_sellers():
    """Test seller lookup"""
    print("\n🔍 Testing seller lookup...")
    
    test_items = [{"name": "Arduino Uno", "quantity": 5}]
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/get-sellers",
            json={"items": test_items}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Get sellers passed")
            if data['data'] and len(data['data']) > 0:
                print(f"   Found {len(data['data'][0].get('sellers', []))} sellers")
            return True
        else:
            print(f"❌ Get sellers failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get sellers error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running Backend Tests\n")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health():
        print("\n⚠️  Backend is not running!")
        print("   Start it with: cd backend && python app.py")
        exit(1)
    
    # Test 2: Parse BOM
    parse_result = test_parse_bom()
    
    # Test 3: Get sellers (may fail if API key not configured)
    seller_result = test_get_sellers()
    
    print("\n" + "=" * 50)
    print("\n📊 Test Summary:")
    print(f"   Health Check: ✅")
    print(f"   Parse BOM: {'✅' if parse_result else '❌'}")
    print(f"   Get Sellers: {'✅' if seller_result else '⚠️  (may need API key)'}")
    
    if parse_result:
        print("\n🎉 Backend is working!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
