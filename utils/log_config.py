import os
import logging

# Set the project root and log file path
project_root = os.path.abspath(os.path.dirname(__file__) + "/..")
log_file_path = os.path.join(project_root, "application.log")


def setup_logging():
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a stream handler (for console output)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger, file_handler


# Set up logging
logger, file_handler = setup_logging()

# Close the file handler to avoid ResourceWarning
file_handler.close()
logger.removeHandler(file_handler)
