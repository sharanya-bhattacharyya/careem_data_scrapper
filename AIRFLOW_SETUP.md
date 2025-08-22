# Airflow Setup Guide for Careem Scraper

This guide provides step-by-step instructions for setting up and deploying the Careem promotional scraper using Apache Airflow.

## Prerequisites

- Apache Airflow 2.7.0 or higher installed
- Python 3.8+ environment
- Access to Airflow web interface
- Valid Careem API authentication tokens

## Step 1: Install Dependencies

### Option A: Install in Airflow Environment
```bash
# Navigate to your Airflow installation directory
cd /path/to/airflow

# Install required packages
pip install requests>=2.31.0 PyYAML>=6.0.1 tenacity>=8.2.3 pytz>=2023.3 pandas>=2.0.0
```

### Option B: Use Requirements File
```bash
# Copy requirements.txt to Airflow environment
cp requirements.txt /path/to/airflow/

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Deploy DAG Files

### Copy Files to DAGs Directory
```bash
# Copy all necessary files to Airflow dags folder
cp airflow_dag.py /path/to/airflow/dags/
cp careem_scraper.py /path/to/airflow/dags/
cp config.yaml /path/to/airflow/dags/
```

### Verify File Structure
Your Airflow dags directory should contain:
```
dags/
├── airflow_dag.py
├── careem_scraper.py
└── config.yaml
```

## Step 3: Configure Authentication

### Update Configuration File
Edit `config.yaml` in the dags directory:

```yaml
auth:
  # Replace with your actual tokens
  authorization: "Bearer YOUR_ACTUAL_TOKEN_HERE"
  session_id: "YOUR_ACTUAL_SESSION_ID"
  appengine_session_id: "YOUR_ACTUAL_APPENGINE_SESSION_ID"
```

### Get Fresh Tokens
1. Use the Careem app to generate fresh authentication tokens
2. Update the `auth` section in `config.yaml`
3. Ensure tokens are valid and not expired

## Step 4: Configure Airflow Settings

### Update DAG Configuration
Edit `airflow_dag.py` and modify:

```python
# Email notifications
default_args = {
    'email': ['your-email@company.com', 'admin@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

# Schedule (optional - default is every 6 hours)
dag = DAG(
    'careem_promotional_scraper',
    schedule_interval='0 */6 * * *',  # Change as needed
    # ... other settings
)
```

### Set Airflow Variables (Optional)
```bash
# Set email notifications
airflow variables set careem_email_notifications "admin@company.com"

# Set output directory
airflow variables set careem_output_directory "/path/to/output"
```

## Step 5: Test DAG

### Validate DAG Syntax
```bash
# Check DAG syntax
python /path/to/airflow/dags/airflow_dag.py

# Or use Airflow CLI
airflow dags test careem_promotional_scraper 2025-01-21
```

### Test Individual Tasks
```bash
# Test configuration validation
airflow tasks test careem_promotional_scraper validate_configuration 2025-01-21

# Test scraping task
airflow tasks test careem_promotional_scraper scrape_careem_promotions 2025-01-21
```

## Step 6: Enable DAG

### Via Airflow Web UI
1. Open Airflow web interface
2. Navigate to DAGs list
3. Find `careem_promotional_scraper`
4. Toggle the DAG to "On"

### Via Airflow CLI
```bash
# Enable the DAG
airflow dags unpause careem_promotional_scraper
```

## Step 7: Monitor Execution

### Check DAG Status
```bash
# List DAG runs
airflow dags list-runs careem_promotional_scraper

# Check task status
airflow tasks list careem_promotional_scraper
```

### View Logs
```bash
# View task logs
airflow tasks logs careem_promotional_scraper scrape_careem_promotions 2025-01-21
```

## Configuration Options

### Schedule Intervals

| Interval | Cron Expression | Description |
|----------|----------------|-------------|
| Every 6 hours | `0 */6 * * *` | Default setting |
| Daily at 2 AM | `0 2 * * *` | Once per day |
| Every 2 hours | `0 */2 * * *` | More frequent |
| Weekdays only | `0 9 * * 1-5` | Business hours |

### Email Notifications

```python
default_args = {
    'email': ['admin@company.com', 'data-team@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}
```

### Retry Configuration

```python
default_args = {
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError` when running DAG
**Solution**: Ensure all files are in the dags directory and dependencies are installed

#### 2. Configuration Errors
**Problem**: DAG fails at configuration validation
**Solution**: Check `config.yaml` format and authentication tokens

#### 3. Permission Errors
**Problem**: Cannot write to output directory
**Solution**: Ensure Airflow has write permissions to output directory

#### 4. Authentication Failures
**Problem**: API calls return 401 errors
**Solution**: Update authentication tokens in `config.yaml`

### Debug Steps

1. **Check DAG Syntax**:
   ```bash
   python -c "import airflow_dag; print('DAG syntax OK')"
   ```

2. **Test Configuration**:
   ```bash
   python -c "import yaml; yaml.safe_load(open('config.yaml'))"
   ```

3. **Verify Dependencies**:
   ```bash
   python -c "import requests, yaml, tenacity, pytz; print('All dependencies OK')"
   ```

4. **Check File Permissions**:
   ```bash
   ls -la /path/to/airflow/dags/
   ```

## Monitoring and Alerts

### Success Notifications
The DAG sends email notifications on successful completion with:
- Number of promotions scraped
- Output file location
- Timestamp of execution

### Failure Alerts
Automatic email alerts are sent when:
- Configuration validation fails
- Scraping encounters errors
- Output validation fails
- Any task fails after retries

### Log Monitoring
Monitor these log files:
- Airflow task logs
- `careem_scraper.log` (if configured)
- Generated report files

## Maintenance

### Regular Tasks
1. **Update Authentication Tokens**: Tokens expire regularly
2. **Monitor Logs**: Check for errors and warnings
3. **Review Output**: Verify data quality and completeness
4. **Cleanup**: Old files are automatically removed after 7 days

### Performance Optimization
1. **Adjust Schedule**: Modify based on data freshness requirements
2. **Rate Limiting**: Adjust in `config.yaml` if needed
3. **Retry Logic**: Modify retry settings for your environment

## Security Considerations

1. **Token Management**: Store authentication tokens securely
2. **File Permissions**: Restrict access to configuration files
3. **Network Security**: Ensure Airflow can access Careem APIs
4. **Log Security**: Avoid logging sensitive information

## Support

For issues with the Airflow DAG:
1. Check Airflow task logs for detailed error messages
2. Verify configuration and authentication settings
3. Test individual tasks to isolate problems
4. Review the main README.md for general troubleshooting
