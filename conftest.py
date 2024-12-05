import shutil
import pytest
import sys
import os
from datetime import datetime
import logging

# Set up the project root path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from utils.log_config import setup_logging

# Path to the reports directory
REPORTS_DIR = os.path.join(project_root, "reports")

def pytest_configure(config):
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Create reports directory if it doesn't exist
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    # Get the current date in ddmmyyyy format
    # current_date = datetime.now().strftime("%d%m%Y")
    report_folder = os.path.join(REPORTS_DIR)

    # # Create a folder with the current date for reports if it doesn't exist
    # if not os.path.exists(report_folder):
    #     os.makedirs(report_folder)

    # Update the pytest options to save reports in the newly created folder
    config.option.htmlpath = os.path.join(report_folder, "report.html")
    config.option.json_report_file = os.path.join(report_folder, "report.json")

    logger.info(f"Saving test reports to {report_folder}")

    # Add test markers
    config.addinivalue_line("markers", "smoke: mark test as a smoke test")
    config.addinivalue_line("markers", "sanity: mark test as a sanity test")

@pytest.fixture(scope="session", autouse=True)
def log_global_env_facts(record_testsuite_property):
    """Log global environment info"""
    logger = logging.getLogger(__name__)
    logger.info("Test session started")
    yield
    logger.info("Test session finished")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    reports_dir = os.path.join(REPORTS_DIR)

    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Move HTML and JSON reports to the reports directory
    if os.path.exists("report.html"):
        shutil.move("report.html", os.path.join(reports_dir, "report.html"))
    if os.path.exists("report.json"):
        shutil.move("report.json", os.path.join(reports_dir, "report.json"))
