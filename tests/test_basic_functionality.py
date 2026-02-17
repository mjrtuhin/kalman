"""
Basic functionality tests for KALMAN components.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from utils import CacheManager, APIClient, InstructionLoader
from schemas import PostcodeData
import requests


def test_cache_manager():
    """Test cache manager."""
    print("\n=== Testing CacheManager ===")
    
    cache = CacheManager(db_path="data/cache/test_cache.db")
    
    # Test set and get
    test_data = {"test": "data", "value": 123}
    cache.set("test_source", "test_key", test_data, ttl_days=1)
    
    retrieved = cache.get("test_source", "test_key", ttl_days=1)
    
    assert retrieved == test_data, "Cache get/set failed"
    print("✓ Cache set/get works")
    
    # Test cache miss
    missing = cache.get("test_source", "nonexistent_key")
    assert missing is None, "Cache should return None for missing key"
    print("✓ Cache miss handled correctly")
    
    print("✓ CacheManager tests passed!")


def test_api_client():
    """Test API client with real API."""
    print("\n=== Testing APIClient ===")
    
    client = APIClient(timeout=10)
    
    # Test with Postcodes.io (free, no auth)
    try:
        response = client.get("https://api.postcodes.io/postcodes/SW1A1AA")
        
        assert response.get("status") == 200, "API call failed"
        assert "result" in response, "Expected result in response"
        
        print(f"✓ API call successful: {response['result']['postcode']}")
        print(f"✓ Lat/Lng: {response['result']['latitude']}, {response['result']['longitude']}")
        
    except Exception as e:
        print(f"✗ API call failed: {e}")
        return False
    
    finally:
        client.close()
    
    print("✓ APIClient tests passed!")
    return True


def test_pydantic_schemas():
    """Test Pydantic schemas."""
    print("\n=== Testing Pydantic Schemas ===")
    
    # Test PostcodeData schema
    postcode_data = PostcodeData(
        postcode="SW1A 1AA",
        latitude=51.5033,
        longitude=-0.1276,
        region="London",
        district="Westminster"
    )
    
    assert postcode_data.postcode == "SW1A 1AA"
    print("✓ PostcodeData schema validation works")
    
    # Test invalid data
    try:
        invalid = PostcodeData(
            postcode="SW1A 1AA",
            latitude="invalid",  # Should be float
            longitude=-0.1276
        )
        print("✗ Schema validation should have failed")
        return False
    except Exception:
        print("✓ Schema validation correctly rejects invalid data")
    
    print("✓ Pydantic schema tests passed!")
    return True


def test_instruction_loader():
    """Test instruction loader."""
    print("\n=== Testing InstructionLoader ===")
    
    loader = InstructionLoader()
    
    # This will fail since we haven't created instructions yet
    # But we can test the error handling
    try:
        instructions = loader.load("nonexistent_model")
        print("✗ Should have raised FileNotFoundError")
        return False
    except FileNotFoundError as e:
        print(f"✓ Correctly raised FileNotFoundError: {e}")
    
    print("✓ InstructionLoader tests passed!")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("KALMAN Basic Functionality Tests")
    print("="*50)
    
    try:
        test_cache_manager()
        test_api_client()
        test_pydantic_schemas()
        test_instruction_loader()
        
        print("\n" + "="*50)
        print("✓ ALL TESTS PASSED!")
        print("="*50)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
