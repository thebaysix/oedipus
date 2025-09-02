#!/usr/bin/env python3
"""
Test script to verify the export API functionality
"""
import requests
import json
import sys

def test_export_api():
    base_url = "http://localhost:8000"
    
    # First, get available comparisons
    print("🔍 Fetching available comparisons...")
    try:
        response = requests.get(f"{base_url}/api/v1/comparisons/")
        response.raise_for_status()
        comparisons = response.json()
        
        if not comparisons:
            print("❌ No comparisons found in database")
            return False
            
        comparison_id = comparisons[0]["id"]
        comparison_name = comparisons[0]["name"]
        print(f"✅ Found comparison: {comparison_name} (ID: {comparison_id})")
        
    except Exception as e:
        print(f"❌ Failed to fetch comparisons: {e}")
        return False
    
    # Test different export formats
    formats_to_test = [
        {
            "format": "summary",
            "include_raw_data": False,
            "include_statistics": True,
            "include_insights": True,
            "include_visualizations": False
        },
        {
            "format": "csv",
            "include_raw_data": True,
            "include_statistics": True,
            "include_insights": False,
            "include_visualizations": False
        },
        {
            "format": "json",
            "include_raw_data": True,
            "include_statistics": True,
            "include_insights": True,
            "include_visualizations": False
        }
    ]
    
    for export_config in formats_to_test:
        print(f"\n📄 Testing {export_config['format'].upper()} export...")
        
        export_request = {
            "comparison_id": comparison_id,
            **export_config
        }
        
        try:
            response = requests.post(
                f"{base_url}/api/v1/comparisons/{comparison_id}/export",
                json=export_request,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            # Check response headers
            content_type = response.headers.get("Content-Type", "")
            content_disposition = response.headers.get("Content-Disposition", "")
            content_length = response.headers.get("Content-Length", "0")
            
            print(f"✅ Export successful!")
            print(f"   Content-Type: {content_type}")
            print(f"   Content-Disposition: {content_disposition}")
            print(f"   Content-Length: {content_length} bytes")
            
            # Show first 200 characters of content
            content_preview = response.text[:200]
            if len(response.text) > 200:
                content_preview += "..."
            print(f"   Content Preview: {content_preview}")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   Response: {e.response.text}")
            return False
    
    print(f"\n🎉 All export tests passed!")
    return True

if __name__ == "__main__":
    success = test_export_api()
    sys.exit(0 if success else 1)