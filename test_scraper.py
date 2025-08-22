#!/usr/bin/env python3
"""
Test script for Careem UAE Promotional Scraper

This script tests the configuration and setup without making actual API calls.
"""

import os
import sys
import yaml
from datetime import datetime
import pytz

def test_configuration():
    """Test if the configuration file is valid."""
    print("🔧 Testing configuration...")
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # Check required sections
        required_sections = ['api', 'scraping', 'output', 'logging', 'auth']
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing required section: {section}")
                return False
            else:
                print(f"✅ Found section: {section}")
        
        # Check API configuration
        if 'base_url' in config['api']:
            print(f"✅ API base URL: {config['api']['base_url']}")
        
        # Check surfaces configuration
        surfaces = config['scraping'].get('surfaces', [])
        print(f"✅ Found {len(surfaces)} surfaces to scrape:")
        for surface in surfaces:
            print(f"   - {surface.get('name', 'unknown')}")
        
        # Check output configuration
        output_dir = config['output'].get('directory', 'output')
        print(f"✅ Output directory: {output_dir}")
        
        return True
        
    except FileNotFoundError:
        print("❌ Configuration file 'config.yaml' not found")
        return False
    except yaml.YAMLError as e:
        print(f"❌ Error parsing configuration: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed."""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        ('requests', 'HTTP requests'),
        ('yaml', 'YAML parsing'),
        ('tenacity', 'Retry logic'),
        ('pytz', 'Timezone handling'),
        ('pandas', 'Data manipulation')
    ]
    
    all_installed = True
    
    for package, description in dependencies:
        try:
            __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"❌ {package} - {description} (not installed)")
            all_installed = False
    
    return all_installed

def test_output_directory():
    """Test if output directory exists and is writable."""
    print("\n📁 Testing output directory...")
    
    output_dir = 'output'
    
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"✅ Created output directory: {output_dir}")
        except Exception as e:
            print(f"❌ Failed to create output directory: {e}")
            return False
    else:
        print(f"✅ Output directory exists: {output_dir}")
    
    # Test if directory is writable
    test_file = os.path.join(output_dir, 'test_write.tmp')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("✅ Output directory is writable")
        return True
    except Exception as e:
        print(f"❌ Output directory is not writable: {e}")
        return False

def test_timestamp_generation():
    """Test timestamp generation in Asia/Dubai timezone."""
    print("\n🕐 Testing timestamp generation...")
    
    try:
        dubai_tz = pytz.timezone('Asia/Dubai')
        timestamp = datetime.now(dubai_tz).isoformat()
        print(f"✅ Generated timestamp: {timestamp}")
        return True
    except Exception as e:
        print(f"❌ Failed to generate timestamp: {e}")
        return False

def test_sample_csv():
    """Test if sample CSV file exists and is readable."""
    print("\n📊 Testing sample CSV file...")
    
    sample_file = 'output/careem_promos_20250121_143000.csv'
    
    if os.path.exists(sample_file):
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1:  # Has header and at least one data row
                    print(f"✅ Sample CSV file exists with {len(lines)-1} data rows")
                    return True
                else:
                    print("❌ Sample CSV file is empty")
                    return False
        except Exception as e:
            print(f"❌ Error reading sample CSV: {e}")
            return False
    else:
        print("❌ Sample CSV file not found")
        return False

def main():
    """Run all tests."""
    print("🧪 Careem UAE Promotional Scraper - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Dependencies", test_dependencies),
        ("Output Directory", test_output_directory),
        ("Timestamp Generation", test_timestamp_generation),
        ("Sample CSV", test_sample_csv)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The scraper is ready to use.")
        print("\nNext steps:")
        print("1. Update authentication tokens in config.yaml")
        print("2. Run: python careem_scraper.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the scraper.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
