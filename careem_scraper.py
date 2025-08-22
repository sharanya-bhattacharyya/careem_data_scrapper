#!/usr/bin/env python3
"""
Careem UAE Promotional Scraper

This script scrapes promotional placements from the Careem UAE app
and saves them to a CSV file with the required format.

Author: AI Assistant
Date: 2025-01-21
"""

import os
import sys
import json
import logging
import time
import csv
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import requests
import yaml
from tenacity import retry, stop_after_attempt, wait_exponential
import pytz


@dataclass
class PromoData:
    """Data class for promotional placement information."""
    surface: str
    placement_type: str
    image_url: str
    scrape_timestamp: str


class CareemScraper:
    """Main scraper class for Careem promotional placements."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the scraper with configuration."""
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self._setup_session()
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            self.logger.error(f"Configuration file {config_path} not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def _setup_session(self):
        """Setup the requests session with headers and authentication."""
        # Set common headers
        headers = self.config['api']['headers'].copy()
        
        # Add authentication headers
        headers.update({
            'authorization': self.config['auth']['authorization'],
            'session_id': self.config['auth']['session_id'],
            'x-careem-session-id': self.config['auth']['session_id'],
            'x-careem-appengine-page-session-id': self.config['auth']['appengine_session_id'],
            'lat': self.config['api']['location']['lat'],
            'lng': self.config['api']['location']['lng'],
            'x-careem-user-location': self.config['api']['location']['user_location'],
            'x-careem-delivery-location': self.config['api']['location']['delivery_location'],
        })
        
        self.session.headers.update(headers)
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_config = self.config['logging']
        logging.basicConfig(
            level=getattr(logging, log_config['level']),
            format=log_config['format'],
            handlers=[
                logging.FileHandler(log_config['file']),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _make_api_request(self, endpoint: str, params: Dict[str, str]) -> Dict[str, Any]:
        """Make API request with retry logic and rate limiting."""
        url = f"{self.config['api']['base_url']}/{endpoint}"
        
        # Rate limiting
        time.sleep(1 / self.config['scraping']['rate_limit']['requests_per_second'])
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            self.logger.info(f"Successfully fetched data from {endpoint}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed for {endpoint}: {e}")
            raise
    
    def _extract_promos_from_response(self, response_data: Dict[str, Any], surface: str) -> List[PromoData]:
        """Extract promotional data from API response."""
        promos = []
        
        try:
            # Navigate through the response structure to find promotional content
            # This is based on typical Careem API response structure
            if 'data' in response_data:
                data = response_data['data']
                
                # Look for promotional modules in the response
                if 'modules' in data:
                    for module in data['modules']:
                        promo_data = self._extract_from_module(module, surface)
                        if promo_data:
                            promos.extend(promo_data)
                
                # Also check for direct promotional content
                if 'promotions' in data:
                    for promo in data['promotions']:
                        promo_data = self._extract_from_promotion(promo, surface)
                        if promo_data:
                            promos.append(promo_data)
            
            # If no structured data found, try to extract from other fields
            if not promos:
                promo_data = self._extract_from_generic_response(response_data, surface)
                if promo_data:
                    promos.extend(promo_data)
                    
        except Exception as e:
            self.logger.error(f"Error extracting promos from {surface}: {e}")
        
        return promos
    
    def _extract_from_module(self, module: Dict[str, Any], surface: str) -> List[PromoData]:
        """Extract promotional data from a module."""
        promos = []
        
        try:
            module_type = module.get('type', 'unknown')
            
            # Check if module contains promotional content
            if 'items' in module:
                for item in module['items']:
                    promo_data = self._extract_from_item(item, surface, module_type)
                    if promo_data:
                        promos.append(promo_data)
            
            # Check for banner or promotional content directly in module
            if 'banner' in module:
                promo_data = self._extract_from_banner(module['banner'], surface, module_type)
                if promo_data:
                    promos.append(promo_data)
                    
        except Exception as e:
            self.logger.error(f"Error extracting from module: {e}")
        
        return promos
    
    def _extract_from_item(self, item: Dict[str, Any], surface: str, module_type: str) -> Optional[PromoData]:
        """Extract promotional data from an item."""
        try:
            # Look for image URL in various possible fields
            image_url = (
                item.get('image_url') or 
                item.get('imageUrl') or 
                item.get('banner_url') or 
                item.get('bannerUrl') or 
                item.get('promo_image') or
                item.get('thumbnail') or
                'N/A'
            )
            
            # Determine placement type based on module type and item structure
            placement_type = self._determine_placement_type(module_type, item)
            
            if image_url and image_url != 'N/A':
                return PromoData(
                    surface=surface,
                    placement_type=placement_type,
                    image_url=image_url,
                    scrape_timestamp=self._get_timestamp()
                )
                
        except Exception as e:
            self.logger.error(f"Error extracting from item: {e}")
        
        return None
    
    def _extract_from_banner(self, banner: Dict[str, Any], surface: str, module_type: str) -> Optional[PromoData]:
        """Extract promotional data from a banner."""
        try:
            image_url = (
                banner.get('image_url') or 
                banner.get('imageUrl') or 
                banner.get('url') or
                'N/A'
            )
            
            placement_type = 'banner'
            
            if image_url and image_url != 'N/A':
                return PromoData(
                    surface=surface,
                    placement_type=placement_type,
                    image_url=image_url,
                    scrape_timestamp=self._get_timestamp()
                )
                
        except Exception as e:
            self.logger.error(f"Error extracting from banner: {e}")
        
        return None
    
    def _extract_from_promotion(self, promo: Dict[str, Any], surface: str) -> Optional[PromoData]:
        """Extract promotional data from a promotion object."""
        try:
            image_url = (
                promo.get('image_url') or 
                promo.get('imageUrl') or 
                promo.get('banner_url') or
                'N/A'
            )
            
            placement_type = promo.get('type', 'promotion')
            
            if image_url and image_url != 'N/A':
                return PromoData(
                    surface=surface,
                    placement_type=placement_type,
                    image_url=image_url,
                    scrape_timestamp=self._get_timestamp()
                )
                
        except Exception as e:
            self.logger.error(f"Error extracting from promotion: {e}")
        
        return None
    
    def _extract_from_generic_response(self, response_data: Dict[str, Any], surface: str) -> List[PromoData]:
        """Extract promotional data from generic response structure."""
        promos = []
        
        try:
            # Recursively search for image URLs in the response
            def find_images(obj, path=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key
                        if 'image' in key.lower() or 'banner' in key.lower() or 'promo' in key.lower():
                            if isinstance(value, str) and value.startswith('http'):
                                promos.append(PromoData(
                                    surface=surface,
                                    placement_type=self._determine_placement_type_from_path(current_path),
                                    image_url=value,
                                    scrape_timestamp=self._get_timestamp()
                                ))
                        else:
                            find_images(value, current_path)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        find_images(item, f"{path}[{i}]")
            
            find_images(response_data)
            
        except Exception as e:
            self.logger.error(f"Error in generic extraction: {e}")
        
        return promos
    
    def _determine_placement_type(self, module_type: str, item: Dict[str, Any]) -> str:
        """Determine placement type based on module type and item structure."""
        module_type_lower = module_type.lower()
        
        if 'banner' in module_type_lower:
            return 'banner'
        elif 'carousel' in module_type_lower:
            return 'carousel'
        elif 'grid' in module_type_lower or 'list' in module_type_lower:
            return 'module'
        elif 'promo' in module_type_lower:
            return 'promotion'
        else:
            return 'module'
    
    def _determine_placement_type_from_path(self, path: str) -> str:
        """Determine placement type from JSON path."""
        path_lower = path.lower()
        
        if 'banner' in path_lower:
            return 'banner'
        elif 'carousel' in path_lower:
            return 'carousel'
        elif 'promo' in path_lower:
            return 'promotion'
        else:
            return 'module'
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in Asia/Dubai timezone."""
        dubai_tz = pytz.timezone(self.config['output']['timezone'])
        return datetime.now(dubai_tz).isoformat()
    
    def scrape_surface(self, surface_config: Dict[str, Any]) -> List[PromoData]:
        """Scrape promotional data from a specific surface."""
        surface_name = surface_config['name']
        endpoint = surface_config['endpoint']
        params = surface_config['params']
        
        self.logger.info(f"Starting to scrape surface: {surface_name}")
        
        try:
            response_data = self._make_api_request(endpoint, params)
            promos = self._extract_promos_from_response(response_data, surface_name)
            
            self.logger.info(f"Scraped {len(promos)} promos from {surface_name}")
            return promos
            
        except Exception as e:
            self.logger.error(f"Failed to scrape surface {surface_name}: {e}")
            return []
    
    def scrape_all_surfaces(self) -> List[PromoData]:
        """Scrape promotional data from all configured surfaces."""
        all_promos = []
        
        for surface_config in self.config['scraping']['surfaces']:
            promos = self.scrape_surface(surface_config)
            all_promos.extend(promos)
            
            # Add delay between surfaces to be respectful
            time.sleep(2)
        
        self.logger.info(f"Total promos scraped: {len(all_promos)}")
        return all_promos
    
    def save_to_csv(self, promos: List[PromoData]) -> str:
        """Save promotional data to CSV file."""
        if not promos:
            self.logger.warning("No promotional data to save")
            return ""
        
        # Create output directory if it doesn't exist
        output_dir = self.config['output']['directory']
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.config['output']['filename_format'].format(timestamp=timestamp)
        filepath = os.path.join(output_dir, filename)
        
        # Write to CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['surface', 'placement_type', 'image_url', 'scrape_timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for promo in promos:
                writer.writerow({
                    'surface': promo.surface,
                    'placement_type': promo.placement_type,
                    'image_url': promo.image_url,
                    'scrape_timestamp': promo.scrape_timestamp
                })
        
        self.logger.info(f"Saved {len(promos)} promos to {filepath}")
        return filepath
    
    def run(self) -> str:
        """Run the complete scraping workflow."""
        self.logger.info("Starting Careem promotional scraper")
        
        try:
            # Scrape all surfaces
            promos = self.scrape_all_surfaces()
            
            # Save to CSV
            if promos:
                filepath = self.save_to_csv(promos)
                self.logger.info(f"Scraping completed successfully. Output: {filepath}")
                return filepath
            else:
                self.logger.warning("No promotional data found")
                return ""
                
        except Exception as e:
            self.logger.error(f"Scraping workflow failed: {e}")
            raise


def main():
    """Main entry point for the script."""
    try:
        scraper = CareemScraper()
        output_file = scraper.run()
        
        if output_file:
            print(f"✅ Scraping completed successfully!")
            print(f"📁 Output file: {output_file}")
        else:
            print("⚠️  No promotional data found")
            
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
