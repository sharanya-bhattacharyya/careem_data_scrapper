#!/usr/bin/env python3
"""
Demo script for Careem UAE Promotional Scraper

This script demonstrates the scraper functionality with simulated data
since actual API calls require valid authentication tokens.
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
import yaml
import pytz


@dataclass
class PromoData:
    """Data class for promotional placement information."""
    surface: str
    placement_type: str
    image_url: str
    scrape_timestamp: str


class DemoCareemScraper:
    """Demo scraper class that simulates the real scraper functionality."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the demo scraper with configuration."""
        self.config = self._load_config(config_path)
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
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in Asia/Dubai timezone."""
        dubai_tz = pytz.timezone(self.config['output']['timezone'])
        return datetime.now(dubai_tz).isoformat()
    
    def _simulate_api_response(self, surface_name: str) -> Dict[str, Any]:
        """Simulate API response data for demonstration purposes."""
        
        # Simulate different response structures for different surfaces
        if surface_name == "homepage":
            return {
                "data": {
                    "modules": [
                        {
                            "type": "banner_module",
                            "items": [
                                {
                                    "image_url": "https://careem-assets.s3.amazonaws.com/promotions/ramadan_banner_2025.jpg",
                                    "title": "Ramadan Special"
                                },
                                {
                                    "image_url": "https://careem-assets.s3.amazonaws.com/promotions/food_delivery_promo.jpg",
                                    "title": "Food Delivery Promo"
                                }
                            ]
                        },
                        {
                            "type": "carousel_module",
                            "items": [
                                {
                                    "image_url": "https://careem-assets.s3.amazonaws.com/promotions/restaurant_week_2025.jpg",
                                    "title": "Restaurant Week"
                                }
                            ]
                        },
                        {
                            "type": "promotion_module",
                            "banner": {
                                "image_url": "https://careem-assets.s3.amazonaws.com/promotions/grocery_discount.jpg",
                                "title": "Grocery Discount"
                            }
                        }
                    ]
                }
            }
        
        elif surface_name == "search":
            return {
                "data": {
                    "modules": [
                        {
                            "type": "search_results",
                            "items": [
                                {
                                    "image_url": "https://careem-assets.s3.amazonaws.com/promotions/burger_search_banner.jpg",
                                    "title": "Burger Search Banner"
                                },
                                {
                                    "image_url": "https://careem-assets.s3.amazonaws.com/promotions/burger_restaurants.jpg",
                                    "title": "Burger Restaurants"
                                }
                            ]
                        }
                    ],
                    "promotions": [
                        {
                            "image_url": "https://careem-assets.s3.amazonaws.com/promotions/burger_deals.jpg",
                            "type": "search_promotion"
                        }
                    ]
                }
            }
        
        elif surface_name == "category_burgers":
            return {
                "data": {
                    "modules": [
                        {
                            "type": "category_banner",
                            "items": [
                                {
                                    "image_url": "https://careem-assets.s3.amazonaws.com/promotions/burger_category_banner.jpg",
                                    "title": "Burger Category"
                                }
                            ]
                        }
                    ]
                }
            }
        
        elif surface_name == "category_groceries":
            return {
                "data": {
                    "modules": [
                        {
                            "type": "grocery_module",
                            "items": [
                                {
                                    "image_url": "https://careem-assets.s3.amazonaws.com/promotions/grocery_category_banner.jpg",
                                    "title": "Grocery Category"
                                }
                            ]
                        }
                    ]
                }
            }
        
        return {"data": {"modules": []}}
    
    def _extract_promos_from_response(self, response_data: Dict[str, Any], surface: str) -> List[PromoData]:
        """Extract promotional data from simulated API response."""
        promos = []
        
        try:
            # Simulate the same extraction logic as the real scraper
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
    
    def scrape_surface(self, surface_config: Dict[str, Any]) -> List[PromoData]:
        """Scrape promotional data from a specific surface (simulated)."""
        surface_name = surface_config['name']
        
        self.logger.info(f"Starting to scrape surface: {surface_name}")
        
        try:
            # Simulate API delay
            time.sleep(1)
            
            # Simulate API response
            response_data = self._simulate_api_response(surface_name)
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
            time.sleep(1)
        
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
        """Run the complete demo scraping workflow."""
        self.logger.info("Starting Careem promotional scraper (DEMO MODE)")
        
        try:
            # Scrape all surfaces
            promos = self.scrape_all_surfaces()
            
            # Save to CSV
            if promos:
                filepath = self.save_to_csv(promos)
                self.logger.info(f"Demo scraping completed successfully. Output: {filepath}")
                return filepath
            else:
                self.logger.warning("No promotional data found")
                return ""
                
        except Exception as e:
            self.logger.error(f"Demo scraping workflow failed: {e}")
            raise


def main():
    """Main entry point for the demo script."""
    try:
        print("🎭 Careem UAE Promotional Scraper - DEMO MODE")
        print("=" * 50)
        print("This is a demonstration of the scraper functionality.")
        print("It uses simulated data since actual API calls require valid tokens.")
        print("=" * 50)
        
        scraper = DemoCareemScraper()
        output_file = scraper.run()
        
        if output_file:
            print(f"\n✅ Demo completed successfully!")
            print(f"📁 Output file: {output_file}")
            print(f"\n📊 Check the generated CSV file to see the scraped data structure.")
        else:
            print("⚠️  No promotional data found in demo")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
