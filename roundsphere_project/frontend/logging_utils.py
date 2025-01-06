import logging
import os
from datetime import datetime
from functools import wraps
import json
import traceback

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
logger = logging.getLogger('frontend')
logger.setLevel(logging.DEBUG)

# Create file handler
log_file = os.path.join(LOGS_DIR, f'frontend_{datetime.now().strftime("%Y%m%d")}.log')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_function_call(func):
    """Decorator to log function entry, exit, and any errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        # Convert args and kwargs to string, handling potential JSON serialization issues
        try:
            args_str = json.dumps(args) if args else ''
            kwargs_str = json.dumps(kwargs) if kwargs else ''
        except TypeError:
            args_str = str(args)
            kwargs_str = str(kwargs)

        logger.debug(f"Entering {func_name} - Args: {args_str}, Kwargs: {kwargs_str}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func_name} - Result: {str(result)[:1000]}")  # Limit result length
            return result
        except Exception as e:
            logger.error(f"Error in {func_name}: {str(e)}\nTraceback:\n{traceback.format_exc()}")
            raise

    return wrapper

def log_request_details(request, prefix=''):
    """Log detailed information about a request"""
    logger.debug(f"{prefix}Request Details:")
    logger.debug(f"{prefix}Method: {request.method}")
    logger.debug(f"{prefix}Path: {request.path}")
    logger.debug(f"{prefix}Headers: {dict(request.headers)}")
    logger.debug(f"{prefix}GET params: {dict(request.GET)}")
    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            body = request.body.decode('utf-8')
            logger.debug(f"{prefix}Body: {body}")
        except:
            logger.debug(f"{prefix}Body: Unable to decode request body")

def log_response_details(response, prefix=''):
    """Log detailed information about a response"""
    logger.debug(f"{prefix}Response Details:")
    logger.debug(f"{prefix}Status Code: {response.status_code}")
    logger.debug(f"{prefix}Headers: {dict(response.headers)}")
    try:
        content = response.content.decode('utf-8')
        logger.debug(f"{prefix}Content: {content[:1000]}")  # Limit content length
    except:
        logger.debug(f"{prefix}Content: Unable to decode response content")

def log_api_request(url, method, headers, data=None, params=None):
    """Log API request details"""
    logger.debug("API Request Details:")
    logger.debug(f"URL: {url}")
    logger.debug(f"Method: {method}")
    logger.debug(f"Headers: {headers}")
    if data:
        logger.debug(f"Data: {json.dumps(data, indent=2)}")
    if params:
        logger.debug(f"Params: {json.dumps(params, indent=2)}")

def log_api_response(response):
    """Log API response details"""
    logger.debug("API Response Details:")
    logger.debug(f"Status Code: {response.status_code}")
    logger.debug(f"Headers: {dict(response.headers)}")
    try:
        content = response.json()
        logger.debug(f"Content: {json.dumps(content, indent=2)}")
    except:
        logger.debug(f"Content: {response.text}")

def log_session_data(request):
    """Log session data safely (excluding sensitive information)"""
    session_data = dict(request.session)
    # Remove sensitive data
    sensitive_keys = ['password', 'csrf_token']
    for key in sensitive_keys:
        if key in session_data:
            session_data[key] = '[REDACTED]'
    logger.debug(f"Session Data: {session_data}")
