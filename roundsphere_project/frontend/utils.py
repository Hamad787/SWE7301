from django.conf import settings
import requests
from requests.exceptions import RequestException
from django.core.exceptions import ValidationError
import json
from urllib.parse import urljoin
from .logging_utils import logger, log_function_call, log_api_request, log_api_response

@log_function_call
def get_api_url(endpoint):
    """Get full API URL for the given endpoint"""
    base = settings.FLASK_API['BASE_URL'].rstrip('/')
    version = settings.FLASK_API['API_VERSION'].strip('/')
    endpoint = endpoint.strip('/')
    
    # All endpoints are under /api/
    url = f"{base}/{version}/{endpoint}"
    logger.debug(f"Generated API URL: {url}")
    return url

@log_function_call
def make_api_request(method, endpoint, token=None, json=None, params=None):
    """Make a request to the Flask API"""
    logger.debug(f"Making {method} request to {endpoint}")
    logger.debug(f"Token: {token}")
    logger.debug(f"JSON data: {json}")
    logger.debug(f"Query params: {params}")
    
    try:
        # Build full URL
        base_url = settings.FLASK_API['BASE_URL']
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        if not endpoint.startswith('/api/'):
            endpoint = '/api' + endpoint
            
        url = urljoin(base_url, endpoint)
        logger.debug(f"Full URL: {url}")
        
        # Set up headers
        headers = {
            'Content-Type': 'application/json'
        }
        if token:
            if not token.startswith('Bearer '):
                token = f'Bearer {token}'
            headers['Authorization'] = token
            
        logger.debug(f"Request headers: {headers}")
        
        # Make request
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            params=params,
            timeout=settings.FLASK_API['TIMEOUT']
        )
        
        # Log response details for debugging
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        try:
            logger.debug(f"Response body: {response.json()}")
        except:
            logger.debug(f"Response text: {response.text}")
        
        # Raise error for bad responses
        response.raise_for_status()
        
        # Return JSON response if possible
        try:
            return response.json()
        except ValueError:
            return response.text
            
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise Exception(f"API request failed: {str(e)}")
    except Exception as e:
        logger.error(f"Error making API request: {str(e)}")
        raise
