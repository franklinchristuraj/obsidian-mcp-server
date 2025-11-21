#!/usr/bin/env python3
"""
Remote MCP Server Connection Diagnostic Tool
Tests the remote server connection and identifies issues
"""
import json
import sys
import httpx
from typing import Dict, Any

# Remote server configuration
REMOTE_URL = "https://mcp.ziksaka.com"
MCP_ENDPOINT = f"{REMOTE_URL}/mcp"
HEALTH_ENDPOINT = f"{REMOTE_URL}/health"
API_KEY = "798f67623306a6e2092542b9bdcf9775b44f5d4ae3193b1a2820b369e194047e"

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_health_endpoint():
    """Test the health endpoint (no auth required)"""
    print_section("1. Testing Health Endpoint")
    try:
        response = httpx.get(HEALTH_ENDPOINT, timeout=10.0)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Health endpoint is accessible")
            return True
        else:
            print(f"   ❌ Health endpoint returned {response.status_code}")
            return False
    except httpx.ConnectError as e:
        print(f"   ❌ Connection Error: {e}")
        print("   💡 Check if the server is running and DNS is resolving")
        return False
    except httpx.TimeoutException:
        print("   ❌ Connection Timeout")
        print("   💡 Server may be down or unreachable")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")
        return False

def test_mcp_ping():
    """Test MCP ping method"""
    print_section("2. Testing MCP Ping Method")
    try:
        request = {
            "jsonrpc": "2.0",
            "method": "ping",
            "id": 1
        }
        
        response = httpx.post(
            MCP_ENDPOINT,
            json=request,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if "error" in result:
                print(f"   ❌ Error in response: {result['error']}")
                return False
            elif "result" in result:
                print("   ✅ Ping method works correctly")
                return True
            else:
                print("   ⚠️  Unexpected response format")
                return False
        else:
            print(f"   ❌ HTTP Error {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP Error: {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tools_list():
    """Test tools/list method"""
    print_section("3. Testing tools/list Method")
    try:
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2
        }
        
        response = httpx.post(
            MCP_ENDPOINT,
            json=request,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
        
        print(f"   Status Code: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            if "error" in result:
                print(f"   ❌ Error: {result['error']}")
                return False
            elif "result" in result and "tools" in result["result"]:
                tools = result["result"]["tools"]
                print(f"   ✅ Retrieved {len(tools)} tools")
                print(f"   Tools: {', '.join([t['name'] for t in tools[:5]])}...")
                return True
            else:
                print(f"   ⚠️  Unexpected response format: {result}")
                return False
        else:
            print(f"   ❌ HTTP Error {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tool_call():
    """Test tools/call method"""
    print_section("4. Testing tools/call Method")
    try:
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "ping",
                "arguments": {}
            },
            "id": 3
        }
        
        response = httpx.post(
            MCP_ENDPOINT,
            json=request,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
        
        print(f"   Status Code: {response.status_code}")
        result = response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            if "error" in result:
                print(f"   ❌ Error: {result['error']}")
                return False
            elif "result" in result:
                print("   ✅ Tool call works correctly")
                return True
            else:
                print("   ⚠️  Unexpected response format")
                return False
        else:
            print(f"   ❌ HTTP Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_authentication():
    """Test authentication methods"""
    print_section("5. Testing Authentication")
    
    # Test without auth
    print("\n   5a. Testing without authentication:")
    try:
        request = {"jsonrpc": "2.0", "method": "ping", "id": 4}
        response = httpx.post(
            MCP_ENDPOINT,
            json=request,
            headers={"Content-Type": "application/json"},
            timeout=10.0
        )
        if response.status_code == 401:
            print("   ✅ Correctly rejects requests without auth")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # Test with invalid auth
    print("\n   5b. Testing with invalid API key:")
    try:
        request = {"jsonrpc": "2.0", "method": "ping", "id": 5}
        response = httpx.post(
            MCP_ENDPOINT,
            json=request,
            headers={
                "Authorization": "Bearer invalid-key",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
        if response.status_code == 401:
            print("   ✅ Correctly rejects invalid API key")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")

def test_error_handling():
    """Test error handling"""
    print_section("6. Testing Error Handling")
    
    # Test invalid method
    print("\n   6a. Testing invalid method:")
    try:
        request = {
            "jsonrpc": "2.0",
            "method": "invalid_method_xyz",
            "id": 6
        }
        response = httpx.post(
            MCP_ENDPOINT,
            json=request,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(result, indent=2)}")
        
        if "error" in result:
            print("   ✅ Error handling works correctly")
        else:
            print("   ⚠️  No error returned for invalid method")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test invalid JSON-RPC
    print("\n   6b. Testing invalid JSON-RPC request:")
    try:
        request = {"method": "ping", "id": 7}  # Missing jsonrpc
        response = httpx.post(
            MCP_ENDPOINT,
            json=request,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(result, indent=2)}")
        
        if "error" in result:
            print("   ✅ Invalid JSON-RPC correctly rejected")
        else:
            print("   ⚠️  Invalid request not rejected")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Run all diagnostic tests"""
    print("\n" + "=" * 60)
    print("  Remote MCP Server Connection Diagnostics")
    print("=" * 60)
    print(f"\n  Server: {REMOTE_URL}")
    print(f"  MCP Endpoint: {MCP_ENDPOINT}")
    print(f"  API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
    
    results = []
    
    # Run tests
    results.append(("Health Endpoint", test_health_endpoint()))
    results.append(("MCP Ping", test_mcp_ping()))
    results.append(("Tools List", test_tools_list()))
    results.append(("Tool Call", test_tool_call()))
    test_authentication()
    test_error_handling()
    
    # Summary
    print_section("Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\n  Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  ✅ All tests passed! Server is functioning correctly.")
        print("\n  💡 If you're still seeing 'UnexpectedError', the issue may be:")
        print("     - Client-side configuration (wrong URL, wrong auth method)")
        print("     - Client library compatibility issue")
        print("     - Network/firewall blocking the connection")
        return 0
    else:
        print("\n  ⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

