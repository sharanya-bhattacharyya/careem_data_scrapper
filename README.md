# Careem UAE Promotional Scraper

A Python workflow to scrape promotional placements from the Careem UAE app and save them to a CSV file. This tool extracts promotional content from various surfaces including homepage, search, and category pages.

## Features

- **Multi-surface scraping**: Homepage, search, and category surfaces
- **Rate limiting**: Respectful API usage with configurable rate limits
- **Error handling**: Robust error handling with retry logic
- **CSV output**: Structured data export with timestamps
- **Logging**: Comprehensive logging for monitoring and debugging
- **Configuration**: YAML-based configuration for easy customization

## Requirements

- Python 3.8 or higher
- Internet connection
- Valid Careem API authentication tokens

## Installation

1. **Clone or download the repository**
   ```bash
   # If you have the files locally, navigate to the project directory
   cd /path/to/assignment
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import requests, yaml, tenacity, pytz; print('All dependencies installed successfully!')"
   ```

## Configuration

### Authentication Setup

The scraper requires valid Careem API authentication tokens. These tokens expire regularly and need to be updated in the `config.yaml` file.

**Important**: The authentication tokens in the current configuration are examples and may be expired. You'll need to:

1. Obtain fresh authentication tokens from the Careem app
2. Update the `auth` section in `config.yaml`:
   ```yaml
   auth:
     authorization: "Bearer YOUR_FRESH_TOKEN_HERE"
     session_id: "YOUR_SESSION_ID"
     appengine_session_id: "YOUR_APPENGINE_SESSION_ID"
   ```

### Configuration File Structure

The `config.yaml` file contains all configuration settings:

```yaml
# API Configuration
api:
  base_url: "https://appengine.careemapis.com/v1/page"
  endpoints:
    homepage: "ea-discovery-home"
    search: "food-hybrid-dishes-search"
  
# Scraping Configuration
scraping:
  surfaces:
    - name: "homepage"
      endpoint: "ea-discovery-home"
      params:
        selectedServiceAreaId: "0"
        refreshCounter: "3"
    
    - name: "search"
      endpoint: "food-hybrid-dishes-search"
      params:
        query: "Burger"

# Output Configuration
output:
  directory: "output"
  filename_format: "careem_promos_{timestamp}.csv"
  timezone: "Asia/Dubai"
```

## Usage

### Basic Usage

Run the scraper with default configuration:

```bash
python careem_scraper.py
```

### Expected Output

The script will:
1. Load configuration from `config.yaml`
2. Scrape promotional data from all configured surfaces
3. Save results to a CSV file in the `output/` directory
4. Log all activities to both console and `careem_scraper.log`

### Output File Format

The CSV file will contain the following columns:
- `surface`: The surface where the promo appears (e.g., "homepage", "search", "category_burgers")
- `placement_type`: Type of placement (e.g., "banner", "module", "carousel")
- `image_url`: URL of the promotional image
- `scrape_timestamp`: Timestamp of the scrape in Asia/Dubai timezone

Example filename: `careem_promos_20250121_143000.csv`

## API Endpoints Used

Based on the existing `.py` files in the repository, the scraper uses these endpoints:

1. **Homepage**: `ea-discovery-home`
   - Used for main homepage promotional content
   - Parameters: `selectedServiceAreaId`, `refreshCounter`

2. **Search**: `food-hybrid-dishes-search`
   - Used for search results and category-specific content
   - Parameters: `query` (e.g., "Burger")

3. **Food Home**: `ea-discovery-home`
   - Used for food-specific homepage content
   - Parameters: `selectedServiceAreaId`, `refreshCounter`

## Assumptions Made

### API Response Structure
- The API responses contain promotional content in a structured format
- Promotional images are accessible via URLs in the response
- The response structure includes modules, items, and promotional objects

### Authentication
- Bearer token authentication is required
- Session IDs and device IDs are needed for API access
- Tokens expire and need regular updates

### Rate Limiting
- API has rate limits that should be respected
- 2 requests per second is a safe default
- Exponential backoff is implemented for retries

### Data Extraction
- Image URLs are found in fields like `image_url`, `imageUrl`, `banner_url`, etc.
- Placement types are inferred from module types and response structure
- Missing image URLs are marked as "N/A"

## Error Handling

The scraper includes comprehensive error handling:

- **Network errors**: Retry with exponential backoff
- **Authentication errors**: Log and continue with other surfaces
- **Invalid responses**: Graceful handling of malformed data
- **Missing data**: Fallback to generic extraction methods

## Logging

Logs are written to both:
- Console output (for real-time monitoring)
- `careem_scraper.log` file (for persistent logging)

Log levels include:
- `INFO`: General operation information
- `WARNING`: Non-critical issues
- `ERROR`: Critical errors that may affect functionality

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```
   Error: 401 Unauthorized
   Solution: Update authentication tokens in config.yaml
   ```

2. **Rate Limiting**
   ```
   Error: 429 Too Many Requests
   Solution: Increase delays in rate_limit configuration
   ```

3. **No Data Found**
   ```
   Warning: No promotional data found
   Solution: Check API response structure or update extraction logic
   ```

4. **Configuration Errors**
   ```
   Error: Configuration file not found
   Solution: Ensure config.yaml exists in the project directory
   ```

### Debug Mode

To enable debug logging, modify the logging level in `config.yaml`:

```yaml
logging:
  level: "DEBUG"
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| requests | >=2.31.0 | HTTP requests |
| PyYAML | >=6.0.1 | Configuration parsing |
| tenacity | >=8.2.3 | Retry logic |
| pytz | >=2023.3 | Timezone handling |
| pandas | >=2.0.0 | Data manipulation (optional) |

## File Structure

```
assignment/
├── careem_scraper.py          # Main scraper script
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── output/                  # Output directory
│   └── careem_promos_*.csv  # Generated CSV files
├── careem_scraper.log       # Log file
└── *.py                     # Original API endpoint examples
```

## Sample Output

The scraper generates CSV files with the following structure:

```csv
surface,placement_type,image_url,scrape_timestamp
homepage,banner,https://example.com/banner1.jpg,2025-01-21T14:30:00+04:00
homepage,module,https://example.com/promo1.jpg,2025-01-21T14:30:00+04:00
search,carousel,https://example.com/carousel1.jpg,2025-01-21T14:30:00+04:00
category_burgers,banner,https://example.com/burger_promo.jpg,2025-01-21T14:30:00+04:00
```

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and research purposes. Please ensure compliance with Careem's terms of service and API usage policies.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs in `careem_scraper.log`
3. Verify your configuration in `config.yaml`
4. Ensure your authentication tokens are valid and up-to-date

## Changelog

### Version 1.0.0 (2025-01-21)
- Initial release
- Multi-surface scraping support
- CSV output with timestamps
- Comprehensive error handling
- Rate limiting and retry logic
