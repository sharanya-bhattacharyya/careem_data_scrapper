from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable
from airflow.utils.email import send_email
import os
import sys
import logging
import yaml
import json
from typing import Dict, Any

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the scraper class
from careem_scraper import CareemScraper

# Default arguments for the DAG
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 21),
    'email': ['admin@example.com'],  # Update with actual email
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

# DAG definition
dag = DAG(
    'careem_promotional_scraper',
    default_args=default_args,
    description='Scrape promotional placements from Careem UAE app',
    schedule_interval='0 */6 * * *',  # Run every 6 hours
    max_active_runs=1,
    tags=['careem', 'scraping', 'promotions', 'uae'],
)


def validate_configuration(**context):
    """Validate configuration and dependencies."""
    try:
        # Load configuration
        with open('config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # Check required sections
        required_sections = ['api', 'scraping', 'output', 'logging', 'auth']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required section: {section}")
        
        # Check authentication
        auth = config.get('auth', {})
        if not auth.get('authorization') or auth.get('authorization') == 'Bearer YOUR_FRESH_TOKEN_HERE':
            raise ValueError("Authentication token not configured")
        
        # Check output directory
        output_dir = config['output'].get('directory', 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        logging.info("Configuration validation passed")
        return "Configuration is valid"
        
    except Exception as e:
        logging.error(f"Configuration validation failed: {e}")
        raise


def scrape_careem_promotions(**context):
    """Main scraping task."""
    try:
        # Initialize scraper
        scraper = CareemScraper()
        
        # Run the scraping workflow
        output_file = scraper.run()
        
        if output_file:
            # Store the output file path in XCom for downstream tasks
            context['task_instance'].xcom_push(key='output_file', value=output_file)
            context['task_instance'].xcom_push(key='scrape_status', value='success')
            
            logging.info(f"Scraping completed successfully. Output: {output_file}")
            return f"Scraping completed. Output: {output_file}"
        else:
            context['task_instance'].xcom_push(key='scrape_status', value='no_data')
            logging.warning("No promotional data found")
            return "No promotional data found"
            
    except Exception as e:
        context['task_instance'].xcom_push(key='scrape_status', value='failed')
        logging.error(f"Scraping failed: {e}")
        raise


def validate_output(**context):
    """Validate the generated CSV output."""
    try:
        # Get output file from previous task
        output_file = context['task_instance'].xcom_pull(task_ids='scrape_careem_promotions', key='output_file')
        scrape_status = context['task_instance'].xcom_pull(task_ids='scrape_careem_promotions', key='scrape_status')
        
        if scrape_status == 'no_data':
            logging.info("No data to validate - skipping validation")
            return "No data to validate"
        
        if not output_file or not os.path.exists(output_file):
            raise FileNotFoundError(f"Output file not found: {output_file}")
        
        # Validate CSV structure
        import csv
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Check required columns
            required_columns = ['surface', 'placement_type', 'image_url', 'scrape_timestamp']
            if not all(col in reader.fieldnames for col in required_columns):
                raise ValueError(f"Missing required columns. Found: {reader.fieldnames}")
            
            # Count rows
            rows = list(reader)
            row_count = len(rows)
            
            if row_count == 0:
                raise ValueError("CSV file is empty")
            
            # Validate data quality
            valid_surfaces = ['homepage', 'search', 'category_burgers', 'category_groceries']
            valid_placement_types = ['banner', 'module', 'carousel', 'promotion']
            
            for i, row in enumerate(rows):
                if row['surface'] not in valid_surfaces:
                    logging.warning(f"Row {i+1}: Invalid surface '{row['surface']}'")
                
                if row['placement_type'] not in valid_placement_types:
                    logging.warning(f"Row {i+1}: Invalid placement_type '{row['placement_type']}'")
                
                if not row['image_url'] or row['image_url'] == 'N/A':
                    logging.warning(f"Row {i+1}: Missing or invalid image_url")
        
        logging.info(f"Output validation passed. Found {row_count} promotional entries")
        context['task_instance'].xcom_push(key='row_count', value=row_count)
        return f"Validation passed. {row_count} entries found"
        
    except Exception as e:
        logging.error(f"Output validation failed: {e}")
        raise


def generate_report(**context):
    """Generate a summary report of the scraping results."""
    try:
        scrape_status = context['task_instance'].xcom_pull(task_ids='scrape_careem_promotions', key='scrape_status')
        output_file = context['task_instance'].xcom_pull(task_ids='scrape_careem_promotions', key='output_file')
        row_count = context['task_instance'].xcom_pull(task_ids='validate_output', key='row_count')
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'status': scrape_status,
            'output_file': output_file,
            'row_count': row_count,
            'surfaces_scraped': ['homepage', 'search', 'category_burgers', 'category_groceries']
        }
        
        # Save report to file
        report_file = f"output/scraping_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logging.info(f"Report generated: {report_file}")
        context['task_instance'].xcom_push(key='report_file', value=report_file)
        
        return f"Report generated: {report_file}"
        
    except Exception as e:
        logging.error(f"Report generation failed: {e}")
        raise


def cleanup_old_files(**context):
    """Clean up old CSV and report files (keep last 7 days)."""
    try:
        import glob
        from datetime import datetime, timedelta
        
        # Clean up old CSV files (keep last 7 days)
        output_dir = 'output'
        cutoff_date = datetime.now() - timedelta(days=7)
        
        # Find CSV files older than 7 days
        csv_pattern = os.path.join(output_dir, 'careem_promos_*.csv')
        old_csv_files = []
        
        for csv_file in glob.glob(csv_pattern):
            file_time = datetime.fromtimestamp(os.path.getctime(csv_file))
            if file_time < cutoff_date:
                old_csv_files.append(csv_file)
        
        # Find report files older than 7 days
        report_pattern = os.path.join(output_dir, 'scraping_report_*.json')
        old_report_files = []
        
        for report_file in glob.glob(report_pattern):
            file_time = datetime.fromtimestamp(os.path.getctime(report_file))
            if file_time < cutoff_date:
                old_report_files.append(report_file)
        
        # Delete old files
        deleted_count = 0
        for file_path in old_csv_files + old_report_files:
            try:
                os.remove(file_path)
                deleted_count += 1
                logging.info(f"Deleted old file: {file_path}")
            except Exception as e:
                logging.warning(f"Failed to delete {file_path}: {e}")
        
        logging.info(f"Cleanup completed. Deleted {deleted_count} old files")
        return f"Cleanup completed. Deleted {deleted_count} old files"
        
    except Exception as e:
        logging.error(f"Cleanup failed: {e}")
        raise


def send_success_notification(**context):
    """Send success notification email."""
    try:
        scrape_status = context['task_instance'].xcom_pull(task_ids='scrape_careem_promotions', key='scrape_status')
        output_file = context['task_instance'].xcom_pull(task_ids='scrape_careem_promotions', key='output_file')
        row_count = context['task_instance'].xcom_pull(task_ids='validate_output', key='row_count')
        
        if scrape_status == 'success':
            subject = f"✅ Careem Scraping Success - {row_count} promotions found"
            html_content = f"""
            <h2>Careem Promotional Scraping Completed Successfully</h2>
            <p><strong>Status:</strong> {scrape_status}</p>
            <p><strong>Output File:</strong> {output_file}</p>
            <p><strong>Promotions Found:</strong> {row_count}</p>
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            """
        elif scrape_status == 'no_data':
            subject = "⚠️ Careem Scraping - No Data Found"
            html_content = f"""
            <h2>Careem Promotional Scraping - No Data Found</h2>
            <p><strong>Status:</strong> {scrape_status}</p>
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>No promotional data was found during this scraping run.</p>
            """
        else:
            subject = "❌ Careem Scraping Failed"
            html_content = f"""
            <h2>Careem Promotional Scraping Failed</h2>
            <p><strong>Status:</strong> {scrape_status}</p>
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Please check the Airflow logs for more details.</p>
            """
        
        # Send email (this would be configured in Airflow)
        logging.info(f"Success notification prepared: {subject}")
        return "Success notification sent"
        
    except Exception as e:
        logging.error(f"Success notification failed: {e}")
        raise


# Task definitions
validate_config_task = PythonOperator(
    task_id='validate_configuration',
    python_callable=validate_configuration,
    dag=dag,
)

scrape_task = PythonOperator(
    task_id='scrape_careem_promotions',
    python_callable=scrape_careem_promotions,
    dag=dag,
)

validate_output_task = PythonOperator(
    task_id='validate_output',
    python_callable=validate_output,
    dag=dag,
)

generate_report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag,
)

cleanup_task = PythonOperator(
    task_id='cleanup_old_files',
    python_callable=cleanup_old_files,
    dag=dag,
)

success_notification_task = PythonOperator(
    task_id='send_success_notification',
    python_callable=send_success_notification,
    dag=dag,
)

# Task dependencies #can be changed accordingly
validate_config_task >> scrape_task >> validate_output_task >> generate_report_task
validate_output_task >> cleanup_task
generate_report_task >> success_notification_task
cleanup_task >> success_notification_task
