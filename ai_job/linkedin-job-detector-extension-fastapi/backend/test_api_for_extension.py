#!/usr/bin/env python3
"""
Test script to validate the Job Analysis API for Chrome Extension integration.
Run this script to test the API endpoints that the extension will use.
"""

import requests
import json
import time
import sys

API_BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("   Please start the server with: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_analyze_endpoint():
    """Test the job analysis endpoint with sample data."""
    print("\n🔍 Testing analyze-job endpoint...")
    
    test_cases = [
        {
            "name": "High Risk Job",
            "data": {
                "job_text": "Easy money opportunity! $5000/week working from home. No experience needed. Send SSN and bank details to get started. Contact: money@get-rich-quick.net",
                "company_url": "",
                "recruiter_email": "",
                "platform_source": "chrome"
            },
            "expected_risk": "high"
        },
        {
            "name": "Safe Job",
            "data": {
                "job_text": "Senior Software Engineer at Google. Competitive salary based on experience. Full benefits package. Apply through official Google careers page.",
                "company_url": "",
                "recruiter_email": "",
                "platform_source": "chrome"
            },
            "expected_risk": "low"
        },
        {
            "name": "Medium Risk Job",
            "data": {
                "job_text": "Marketing Assistant position. $50,000 salary. Some requirements unclear. Remote work available.",
                "company_url": "",
                "recruiter_email": "",
                "platform_source": "chrome"
            },
            "expected_risk": "medium"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['name']}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/analyze-job",
                json=test_case["data"],
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Status: {response.status_code}")
                print(f"   📊 Verdict: {result.get('verdict', 'N/A')}")
                print(f"   🎯 Risk Score: {result.get('risk_score', 'N/A')}/100")
                print(f"   🚩 Flags: {len(result.get('flags', []))} warning(s)")
                
                # Validate response structure
                required_fields = ['verdict', 'risk_score', 'flags', 'explanation']
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    print(f"   ⚠️  Missing fields: {missing_fields}")
                else:
                    print("   ✅ Response structure valid")
                    
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Request error: {e}")
        
        # Small delay between requests
        time.sleep(0.5)

def test_error_scenarios():
    """Test error handling scenarios."""
    print("\n🔍 Testing error scenarios...")
    
    # Test empty request
    print("\n   Test: Empty request body")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/analyze-job",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"   Status: {response.status_code} (expected: 422)")
        if response.status_code == 422:
            print("   ✅ Validation error handled correctly")
        else:
            print("   ⚠️  Unexpected response")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test malformed JSON
    print("\n   Test: Malformed JSON")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/analyze-job",
            data='{"invalid": json}',
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"   Status: {response.status_code} (expected: 400)")
        if response.status_code == 400:
            print("   ✅ JSON parsing error handled correctly")
        else:
            print("   ⚠️  Unexpected response")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_rate_limiting():
    """Test rate limiting (if enabled)."""
    print("\n🔍 Testing rate limiting...")
    print("   Making multiple rapid requests...")
    
    test_data = {
        "job_text": "Test job description for rate limiting",
        "company_url": "",
        "recruiter_email": "",
        "platform_source": "chrome"
    }
    
    success_count = 0
    rate_limited = False
    
    for i in range(10):  # Try 10 rapid requests
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/analyze-job",
                json=test_data,
                timeout=5
            )
            
            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 429:
                rate_limited = True
                print(f"   ✅ Rate limiting triggered at request {i+1}")
                break
            else:
                print(f"   ⚠️  Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Request {i+1} error: {e}")
            break
    
    print(f"   📊 Successful requests: {success_count}")
    if rate_limited:
        print("   ✅ Rate limiting is working")
    else:
        print("   ℹ️  Rate limiting not triggered (may be disabled or limit not reached)")

def main():
    """Run all tests."""
    print("🚀 Starting API validation tests for Chrome Extension")
    print("=" * 60)
    
    # Test health endpoint first
    if not test_health_endpoint():
        print("\n❌ Cannot proceed with tests - API server not accessible")
        sys.exit(1)
    
    # Test main functionality
    test_analyze_endpoint()
    
    # Test error scenarios
    test_error_scenarios()
    
    # Test rate limiting
    test_rate_limiting()
    
    print("\n" + "=" * 60)
    print("🎉 API validation tests completed!")
    print("\n📋 Next steps:")
    print("1. Load the Chrome extension from chrome-extension/ folder")
    print("2. Test the extension popup with various job descriptions")
    print("3. Verify error handling in the extension UI")
    print("4. Check browser console for any JavaScript errors")

if __name__ == "__main__":
    main()