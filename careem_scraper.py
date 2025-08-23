
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
    
    def _get_headers_for_surface(self, surface: str) -> Dict[str, str]:
        """Get headers for a specific surface based on working examples."""
        # Base headers that are common across all surfaces
        base_headers = {
            'x-careem-agent': 'ICMA',
            'x-careem-beta': 'false',
            'user-agent': 'ICMA/25.32.0',
            'agent': 'ICMA',
            'time-zone': 'Asia/Dubai',
            'x-careem-appengine-api-version': '2025-07-07',
            'x-careem-operating-system': 'iOS/18.6.1',
            'x-careem-permissions': 'location:granted',
            'accept-language': 'en',
            'x-careem-device-id': 'D0Do1cW3V2mftjsX',
            'accept': '*/*',
        }
        
        # Surface-specific configurations based on working examples
        surface_configs = {
            'homepage': {
                'session_id': '68BE8F88-7CD2-4890-A24C-96E20E4EF9EE',
                'x-careem-session-id': '68BE8F88-7CD2-4890-A24C-96E20E4EF9EE',
                'x-careem-appengine-page-session-id': '8c3d87ea-410f-4865-85af-f81a5418074b',
                'version': '25.32.0',
                'x-careem-version': '25.32.0',
                'x-careem-user-location': '25.25429866282875,55.29878677233094',
                'x-careem-delivery-location': '25.25429866282875,55.29878677233094',
                'lat': '25.25429866282875',
                'lng': '55.29878677233094',
                'authorization': 'Bearer eyJraWQiOiJlYTU4Y2VlZS0yMmU2LTRhNzEtYjkzOS0xNWE3N2IzNzQ3MGMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NTk1MTE4OCwiaWF0IjoxNzU1ODY0Nzg4LCJqdGkiOiIzMzVkNTQ2OC1jNDk2LTRmY2MtYTNiZS1lNDIzYTA2MDI5NGYifQ.naeAHsgNBesdMYKGVAsUsEzKOuuyORO6_G_0un9czEMRISPRHXquIPi2bE8GfCiU9HHrsLEy7fpbNgCKyxRHQrmIU5SLJJDLU9EEy38KBNA89nHv-fmEDOWl5ZdUa-56dfk1JRW7-qYXlqDKibxnf109fjvfF5fuAonWNyZ_a4PPwmyEF1PgR2q4NgToIV2PE2HHsqrZ46wdrLLdYsGieRnYFYz_hQVVOlFUkgrKMnjL3Mrer4aCIIpArGYKbOKu8VUBhYkAgsi9ogbZRxyvgpYWF396zxzlHs2tV-IZVqk9Fxul2328-U5YOKTEfhqxIV1OkSbwBEjxDhjJvZOHbg'
            },
            'food_home': {
                'session_id': '21C7750A-962F-4DDC-B62E-3DA1C8CA828F',
                'x-careem-session-id': '21C7750A-962F-4DDC-B62E-3DA1C8CA828F',
                'x-careem-appengine-page-session-id': 'dc00ad78-5509-492c-975f-3d4cc6c24945',
                'version': '25.32.0',
                'x-careem-version': '25.32.0',
                'x-careem-user-location': '25.25429965142188,55.29878644330265',
                'x-careem-delivery-location': '25.25429965142188,55.29878644330265',
                'lat': '25.25429965142188',
                'lng': '55.29878644330265',
                'authorization': 'Bearer eyJraWQiOiIzOGU2OTcxMS03MjFiLTQxMTctYmUxNi02Y2Y0ZjkzOTAyZWMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NjA1MzAyMywiaWF0IjoxNzU1OTY2NjIzLCJqdGkiOiI5ZGI1OWJjZi1lYTg2LTRiMTEtYjBkZi1jOWY4MWZkNjBjYjAifQ.YZY61hclPjNGXjFtYnv2vaW905gfKLJIv0UYEy4ajDfm5h-HOP0jsQWKkWxYl9P3FnBkYSAsjk5AbaGoS-dWNiXiYeCrb1JrnFK0xUikCiob1p3YcxevvSp6teLYAkSPHqeazP0yruT1lrup0bnsqCwvqCoYNaOj8VZsbVrBxyaLg2cggvJqyWzqlm90q_bR-DK_zc0XhJfpyMB_K-O9bo7hH-OPyxJ7J9Gq9IPmkZjJNy1xMIAuTdU7CQP1UkL2PXFYEAfybsstqFDOOSqXDWAa7m87CKdz5M__TIA1sgRbKzFbVncuAnVQbukRoL6SRu7zfBl6bnE7olozePFptA'
            },
            'search': {
                'session_id': '21C7750A-962F-4DDC-B62E-3DA1C8CA828F',
                'x-careem-session-id': '21C7750A-962F-4DDC-B62E-3DA1C8CA828F',
                'x-careem-appengine-page-session-id': '101fbfc5-f691-4bcd-b76b-9becb5b2239c',
                'version': '25.32.0',
                'x-careem-version': '25.32.0',
                'x-careem-user-location': '25.25429965142188,55.29878644330265',
                'x-careem-delivery-location': '25.25429965142188,55.29878644330265',
                'lat': '25.25429965142188',
                'lng': '55.29878644330265',
                'authorization': 'Bearer eyJraWQiOiIzOGU2OTcxMS03MjFiLTQxMTctYmUxNi02Y2Y0ZjkzOTAyZWMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NjA1MzAyMywiaWF0IjoxNzU1OTY2NjIzLCJqdGkiOiI5ZGI1OWJjZi1lYTg2LTRiMTEtYjBkZi1jOWY4MWZkNjBjYjAifQ.YZY61hclPjNGXjFtYnv2vaW905gfKLJIv0UYEy4ajDfm5h-HOP0jsQWKkWxYl9P3FnBkYSAsjk5AbaGoS-dWNiXiYeCrb1JrnFK0xUikCiob1p3YcxevvSp6teLYAkSPHqeazP0yruT1lrup0bnsqCwvqCoYNaOj8VZsbVrBxyaLg2cggvJqyWzqlm90q_bR-DK_zc0XhJfpyMB_K-O9bo7hH-OPyxJ7J9Gq9IPmkZjJNy1xMIAuTdU7CQP1UkL2PXFYEAfybsstqFDOOSqXDWAa7m87CKdz5M__TIA1sgRbKzFbVncuAnVQbukRoL6SRu7zfBl6bnE7olozePFptA'
            },
            'grocery': {
                'session_id': 'A0413A6A-62DD-457D-A721-CE25DDB8EA95',
                'x-careem-session-id': 'A0413A6A-62DD-457D-A721-CE25DDB8EA95',
                'x-careem-appengine-page-session-id': 'af9cc31c-cf7f-4a43-b4af-850e705e92e5',
                'version': '25.32.0',
                'x-careem-version': '25.32.0',
                'x-careem-user-location': '25.25427759908695,55.298776468959815',
                'x-careem-delivery-location': '25.25427759908695,55.298776468959815',
                'lat': '25.25427759908695',
                'lng': '55.298776468959815',
                'authorization': 'Bearer eyJraWQiOiIzOGU2OTcxMS03MjFiLTQxMTctYmUxNi02Y2Y0ZjkzOTAyZWMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NjA1MzAyMywiaWF0IjoxNzU1OTY2NjIzLCJqdGkiOiI5ZGI1OWJjZi1lYTg2LTRiMTEtYjBkZi1jOWY4MWZkNjBjYjAifQ.YZY61hclPjNGXjFtYnv2vaW905gfKLJIv0UYEy4ajDfm5h-HOP0jsQWKkWxYl9P3FnBkYSAsjk5AbaGoS-dWNiXiYeCrb1JrnFK0xUikCiob1p3YcxevvSp6teLYAkSPHqeazP0yruT1lrup0bnsqCwvqCoYNaOj8VZsbVrBxyaLg2cggvJqyWzqlm90q_bR-DK_zc0XhJfpyMB_K-O9bo7hH-OPyxJ7J9Gq9IPmkZjJNy1xMIAuTdU7CQP1UkL2PXFYEAfybsstqFDOOSqXDWAa7m87CKdz5M__TIA1sgRbKzFbVncuAnVQbukRoL6SRu7zfBl6bnE7olozePFptA'
            },
            'category_burgers': {
                'session_id': '21C7750A-962F-4DDC-B62E-3DA1C8CA828F',
                'x-careem-session-id': '21C7750A-962F-4DDC-B62E-3DA1C8CA828F',
                'x-careem-appengine-page-session-id': '101fbfc5-f691-4bcd-b76b-9becb5b2239c',
                'version': '25.32.0',
                'x-careem-version': '25.32.0',
                'x-careem-user-location': '25.25429965142188,55.29878644330265',
                'x-careem-delivery-location': '25.25429965142188,55.29878644330265',
                'lat': '25.25429965142188',
                'lng': '55.29878644330265',
                'authorization': 'Bearer eyJraWQiOiIzOGU2OTcxMS03MjFiLTQxMTctYmUxNi02Y2Y0ZjkzOTAyZWMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NjA1MzAyMywiaWF0IjoxNzU1OTY2NjIzLCJqdGkiOiI5ZGI1OWJjZi1lYTg2LTRiMTEtYjBkZi1jOWY4MWZkNjBjYjAifQ.YZY61hclPjNGXjFtYnv2vaW905gfKLJIv0UYEy4ajDfm5h-HOP0jsQWKkWxYl9P3FnBkYSAsjk5AbaGoS-dWNiXiYeCrb1JrnFK0xUikCiob1p3YcxevvSp6teLYAkSPHqeazP0yruT1lrup0bnsqCwvqCoYNaOj8VZsbVrBxyaLg2cggvJqyWzqlm90q_bR-DK_zc0XhJfpyMB_K-O9bo7hH-OPyxJ7J9Gq9IPmkZjJNy1xMIAuTdU7CQP1UkL2PXFYEAfybsstqFDOOSqXDWAa7m87CKdz5M__TIA1sgRbKzFbVncuAnVQbukRoL6SRu7zfBl6bnE7olozePFptA'
            },
            'category_groceries': {
                'session_id': 'A0413A6A-62DD-457D-A721-CE25DDB8EA95',
                'x-careem-session-id': 'A0413A6A-62DD-457D-A721-CE25DDB8EA95',
                'x-careem-appengine-page-session-id': 'af9cc31c-cf7f-4a43-b4af-850e705e92e5',
                'version': '25.32.0',
                'x-careem-version': '25.32.0',
                'x-careem-user-location': '25.25427759908695,55.298776468959815',
                'x-careem-delivery-location': '25.25427759908695,55.298776468959815',
                'lat': '25.25427759908695',
                'lng': '55.298776468959815',
                'authorization': 'Bearer eyJraWQiOiIzOGU2OTcxMS03MjFiLTQxMTctYmUxNi02Y2Y0ZjkzOTAyZWMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NjA1MzAyMywiaWF0IjoxNzU1OTY2NjIzLCJqdGkiOiI5ZGI1OWJjZi1lYTg2LTRiMTEtYjBkZi1jOWY4MWZkNjBjYjAifQ.YZY61hclPjNGXjFtYnv2vaW905gfKLJIv0UYEy4ajDfm5h-HOP0jsQWKkWxYl9P3FnBkYSAsjk5AbaGoS-dWNiXiYeCrb1JrnFK0xUikCiob1p3YcxevvSp6teLYAkSPHqeazP0yruT1lrup0bnsqCwvqCoYNaOj8VZsbVrBxyaLg2cggvJqyWzqlm90q_bR-DK_zc0XhJfpyMB_K-O9bo7hH-OPyxJ7J9Gq9IPmkZjJNy1xMIAuTdU7CQP1UkL2PXFYEAfybsstqFDOOSqXDWAa7m87CKdz5M__TIA1sgRbKzFbVncuAnVQbukRoL6SRu7zfBl6bnE7olozePFptA'
            }
        }
        
        # Get surface-specific config or use homepage as default
        surface_config = surface_configs.get(surface, surface_configs['homepage'])
        
        # Merge base headers with surface-specific headers
        headers = {**base_headers, **surface_config}
        return headers
    
    def _get_cookies_for_surface(self, surface: str) -> Dict[str, str]:
        """Get cookies for a specific surface based on working examples."""
        # Surface-specific cookies based on working examples
        surface_cookies = {
            'homepage': {
                '__cf_bm': 'Bj.sFqM3t5VlweBXfNy4TaCbRhlp6FsR8BghvasqUgE-1755944153-1.0.1.1-vMcfN62Z7R3Ha1Aj.lITbZ3SsfjAZ.B1MwiZ1lyaIyaJqf5NhYNkVxMUHrFwcCjHlY01yxyXbTY6tIwoIovmw1fH9eCrDjvuSHbm50d8t6Y'
            },
            'food_home': {
                '_cfuvid': 'xMWRgNv.Q7Hqi0dwbNyXDTadlU.pZ_wWPdVI6Yp_u5Q-1755968052094-0.0.1.1-604800000',
                'dtCookiez48j3ehh': 'v_4_srv_4_sn_50CC5D85F82345BA404FA486851C035A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
                '__cf_bm': 'QOQt1JGSRcyZKty7apjQPNLX1eSoowuzuwUn2bPpchM-1755968015-1.0.1.1-vwjkE0WC0qYeMMt6YHcGrD73iNZfx_ibTODMfI.RTT82jxzx1deBoM7gov6MYkgiFUaZqiy0yMyAScAbZE2PUGfSKxCVZi660NDbFac7hRw'
            },
            'search': {
                '_cfuvid': 'xMWRgNv.Q7Hqi0dwbNyXDTadlU.pZ_wWPdVI6Yp_u5Q-1755968052094-0.0.1.1-604800000',
                'dtCookiez48j3ehh': 'v_4_srv_4_sn_50CC5D85F82345BA404FA486851C035A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
                '__cf_bm': 'QOQt1JGSRcyZKty7apjQPNLX1eSoowuzuwUn2bPpchM-1755968015-1.0.1.1-vwjkE0WC0qYeMMt6YHcGrD73iNZfx_ibTODMfI.RTT82jxzx1deBoM7gov6MYkgiFUaZqiy0yMyAScAbZE2PUGfSKxCVZi660NDbFac7hRw'
            },
            'grocery': {
                '_cfuvid': 'U7BB98yk5bmHOdmMnnn4qzOskWVjgjLr0NcbhQQ8xl4-1755968988869-0.0.1.1-604800000',
                'dtCookiez48j3ehh': 'v_4_srv_4_sn_179CEEA3D2F0B156337696B73F4F8F9A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
                '__cf_bm': 'MqYljBwQHn3UX6DyotZlivzrraNIr1v7BiINuMRt.Dk-1755968980-1.0.1.1-MtAsAn5Zzxrp2ujP89VCDrhUAS1i1r9RxsB0s5GtVjIT7EpJqMg1UG0Wsfk98YurmSah2QakM.4cZx8D34.WL_EtIlviFrFpl0q4RjkAp2E'
            },
            'category_burgers': {
                '_cfuvid': 'xMWRgNv.Q7Hqi0dwbNyXDTadlU.pZ_wWPdVI6Yp_u5Q-1755968052094-0.0.1.1-604800000',
                'dtCookiez48j3ehh': 'v_4_srv_4_sn_50CC5D85F82345BA404FA486851C035A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
                '__cf_bm': 'QOQt1JGSRcyZKty7apjQPNLX1eSoowuzuwUn2bPpchM-1755968015-1.0.1.1-vwjkE0WC0qYeMMt6YHcGrD73iNZfx_ibTODMfI.RTT82jxzx1deBoM7gov6MYkgiFUaZqiy0yMyAScAbZE2PUGfSKxCVZi660NDbFac7hRw'
            },
            'category_groceries': {
                '_cfuvid': 'U7BB98yk5bmHOdmMnnn4qzOskWVjgjLr0NcbhQQ8xl4-1755968988869-0.0.1.1-604800000',
                'dtCookiez48j3ehh': 'v_4_srv_4_sn_179CEEA3D2F0B156337696B73F4F8F9A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
                '__cf_bm': 'MqYljBwQHn3UX6DyotZlivzrraNIr1v7BiINuMRt.Dk-1755968980-1.0.1.1-MtAsAn5Zzxrp2ujP89VCDrhUAS1i1r9RxsB0s5GtVjIT7EpJqMg1UG0Wsfk98YurmSah2QakM.4cZx8D34.WL_EtIlviFrFpl0q4RjkAp2E'
            }
        }
        
        # Get surface-specific cookies or use homepage as default
        return surface_cookies.get(surface, surface_cookies['homepage'])
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _make_api_request(self, endpoint: str, params: Dict[str, str], surface: str) -> Dict[str, Any]:
        """Make API request with retry logic and rate limiting."""
        url = f"{self.config['api']['base_url']}/{endpoint}"
        
        # Get surface-specific headers and cookies
        headers = self._get_headers_for_surface(surface)
        cookies = self._get_cookies_for_surface(surface)
        
        # Rate limiting
        time.sleep(1 / self.config['scraping']['rate_limit']['requests_per_second'])
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed for {endpoint}: {e}")
            raise
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in the configured timezone."""
        tz = pytz.timezone(self.config['output']['timezone'])
        return datetime.now(tz).isoformat()
    
    def _extract_promos_from_response(self, response_data: Dict[str, Any], surface: str) -> List[PromoData]:
        """Extract promotional data from API response."""
        promos = []
        
        try:
            # Navigate to the content structure
            if 'body' in response_data and 'content' in response_data['body']:
                content = response_data['body']['content']
            elif 'content' in response_data:
                content = response_data['content']
            else:
                self.logger.warning(f"No content found in response for surface: {surface}")
                return promos
            
            # Extract from each module
            for module in content:
                if isinstance(module, dict) and 'content' in module:
                    module_promos = self._extract_from_module(module, surface)
                    promos.extend(module_promos)
            
            # Also try generic extraction for any missed items
            generic_promos = self._extract_from_generic_response(response_data, surface)
            promos.extend(generic_promos)
            
        except Exception as e:
            self.logger.error(f"Error extracting promos from response: {e}")
        
        return promos
    
    def _extract_from_module(self, module: Dict[str, Any], surface: str) -> List[PromoData]:
        """Extract promotional data from a module."""
        promos = []
        module_type = module.get('type', 'unknown')
        
        try:
            if 'content' in module and isinstance(module['content'], list):
                for item in module['content']:
                    if isinstance(item, dict):
                        promo = self._extract_from_item(item, surface, module_type)
                        if promo:
                            promos.append(promo)
        except Exception as e:
            self.logger.error(f"Error extracting from module: {e}")
        
        return promos
    
    def _extract_from_item(self, item: Dict[str, Any], surface: str, module_type: str) -> Optional[PromoData]:
        """Extract promotional data from an item."""
        try:
            # Look for image URL in various possible fields
            image_url = None
            
            # Check for direct image_url field (most common in Careem responses)
            if 'image_url' in item:
                image_url = item['image_url']
            
            # Check for image object structure
            elif 'image' in item and isinstance(item['image'], dict):
                image_url = (
                    item['image'].get('image_url_high_res') or
                    item['image'].get('image_url') or
                    item['image'].get('imageUrl')
                )
            
            # Check for leading_content structure
            elif 'leading_content' in item and isinstance(item['leading_content'], dict):
                image_url = (
                    item['leading_content'].get('image_url_high_res') or
                    item['leading_content'].get('image_url') or
                    item['leading_content'].get('imageUrl')
                )
            
            # Check for image_urls array
            elif 'image_urls' in item and isinstance(item['image_urls'], list) and len(item['image_urls']) > 0:
                image_url = item['image_urls'][0]
            
            # Check for background_media
            elif 'background_media' in item and isinstance(item['background_media'], dict):
                image_url = item['background_media'].get('url')
            
            # Fallback to other possible fields
            if not image_url:
                image_url = (
                    item.get('image_url_high_res') or
                    item.get('imageUrl') or 
                    item.get('banner_url') or 
                    item.get('bannerUrl') or 
                    item.get('promo_image') or
                    item.get('thumbnail_url') or
                    item.get('thumbnail') or
                    item.get('url')
                )
            
            # Determine placement type
            placement_type = self._determine_placement_type(module_type, item)
            
            if image_url and image_url != 'N/A' and image_url.startswith('http'):
                return PromoData(
                    surface=surface,
                    placement_type=placement_type,
                    image_url=image_url,
                    scrape_timestamp=self._get_timestamp()
                )
                
        except Exception as e:
            self.logger.error(f"Error extracting from item: {e}")
        
        return None
    
    def _determine_placement_type(self, module_type: str, item: Dict[str, Any]) -> str:
        """Determine placement type based on module type and item structure."""
        # Map module types to placement types
        type_mapping = {
            'tile-carousel': 'carousel',
            'product_list': 'product_list',
            'grocery_list': 'grocery_list',
            'rich-carousel': 'rich_carousel',
            'banner': 'banner',
            'promotion': 'promotion',
            'suggestion': 'suggestion'
        }
        
        # Check if item has specific type indicators
        if 'content_category' in item.get('event_configuration', {}).get('extras', {}):
            return item['event_configuration']['extras']['content_category']
        
        # Use module type mapping
        return type_mapping.get(module_type, 'module')
    
    def _extract_from_generic_response(self, response_data: Dict[str, Any], surface: str) -> List[PromoData]:
        """Extract promotional data from generic response structure."""
        promos = []
        
        def extract_from_dict(data: Dict[str, Any], path: str = ""):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                # Handle image_urls array
                if key == 'image_urls' and isinstance(value, list):
                    for i, img_url in enumerate(value):
                        if img_url and img_url.startswith('http'):
                            promos.append(PromoData(
                                surface=surface,
                                placement_type='generic',
                                image_url=img_url,
                                scrape_timestamp=self._get_timestamp()
                            ))
                
                # Handle image objects
                elif key == 'image' and isinstance(value, dict):
                    img_url = (
                        value.get('image_url_high_res') or
                        value.get('image_url') or
                        value.get('imageUrl')
                    )
                    if img_url and img_url.startswith('http'):
                        promos.append(PromoData(
                            surface=surface,
                            placement_type='image',
                            image_url=img_url,
                            scrape_timestamp=self._get_timestamp()
                        ))
                
                # Handle background_media
                elif key == 'background_media' and isinstance(value, dict):
                    img_url = value.get('url')
                    if img_url and img_url.startswith('http'):
                        promos.append(PromoData(
                            surface=surface,
                            placement_type='background_media',
                            image_url=img_url,
                            scrape_timestamp=self._get_timestamp()
                        ))
                
                # Handle direct image URL fields
                elif any(img_key in key.lower() for img_key in ['image_url', 'banner_url', 'promo_url', 'thumbnail_url']):
                    if isinstance(value, str) and value.startswith('http'):
                        # Avoid duplicates
                        if not any(p.image_url == value for p in promos):
                            promos.append(PromoData(
                                surface=surface,
                                placement_type='direct_url',
                                image_url=value,
                                scrape_timestamp=self._get_timestamp()
                            ))
                
                # Recursively process nested dictionaries
                elif isinstance(value, dict):
                    extract_from_dict(value, current_path)
                
                # Recursively process lists
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            extract_from_dict(item, f"{current_path}[{i}]")
        
        try:
            extract_from_dict(response_data)
        except Exception as e:
            self.logger.error(f"Error in generic extraction: {e}")
        
        return promos
    
    def scrape_surface(self, surface: str) -> List[PromoData]:
        """Scrape a specific surface."""
        self.logger.info(f"Starting to scrape surface: {surface}")
        
        try:
            # Get surface configuration
            surface_config = next(
                (s for s in self.config['scraping']['surfaces'] if s['name'] == surface),
                None
            )
            
            if not surface_config:
                self.logger.error(f"Surface configuration not found for: {surface}")
                return []
            
            # Make API request
            response_data = self._make_api_request(
                surface_config['endpoint'],
                surface_config['params'],
                surface
            )
            
            # Extract promotional data
            promos = self._extract_promos_from_response(response_data, surface)
            
            self.logger.info(f"Extracted {len(promos)} promotional items from {surface}")
            return promos
            
        except Exception as e:
            self.logger.error(f"Failed to scrape surface {surface}: {e}")
            return []
    
    def scrape_all_surfaces(self) -> List[PromoData]:
        """Scrape all configured surfaces."""
        all_promos = []
        
        for surface_config in self.config['scraping']['surfaces']:
            surface_name = surface_config['name']
            promos = self.scrape_surface(surface_name)
            all_promos.extend(promos)
            
            # Add delay between surfaces
            time.sleep(2)
        
        return all_promos
    
    def save_to_csv(self, promos: List[PromoData], filename: str = None) -> str:
        """Save promotional data to CSV file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.config['output']['filename_format'].format(timestamp=timestamp)
        
        # Ensure output directory exists
        os.makedirs(self.config['output']['directory'], exist_ok=True)
        filepath = os.path.join(self.config['output']['directory'], filename)
        
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
                    'scrape_timestamp': promo.scrape_timestamp,
                })
        
        self.logger.info(f"Saved {len(promos)} promotional items to {filepath}")
        return filepath


def main():
    """Main function to run the scraper."""
    scraper = CareemScraper()
    
    print(" Starting Careem promotional scraper")
    
    # Scrape all surfaces
    promos = scraper.scrape_all_surfaces()
    
    if promos:
        # Save to CSV
        filepath = scraper.save_to_csv(promos)
        print(f"Successfully scraped {len(promos)} promotional items")
        print(f"Results saved to: {filepath}")
    else:
        print("No promotional data found")


if __name__ == "__main__":
    main()
