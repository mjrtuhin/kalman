"""
HTTP client with retry logic for API calls.
"""

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """HTTP client with automatic retries and error handling."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize API client.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        GET request with retry logic.
        
        Args:
            url: Request URL
            params: Query parameters
            headers: Request headers
            
        Returns:
            Response JSON as dict
            
        Raises:
            httpx.HTTPError: If request fails after retries
        """
        try:
            logger.info(f"GET {url}")
            response = self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error for {url}: {e}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def post(self, url: str, data: Optional[Dict[str, Any]] = None,
             json_data: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        POST request with retry logic.
        
        Args:
            url: Request URL
            data: Form data
            json_data: JSON data
            headers: Request headers
            
        Returns:
            Response JSON as dict
        """
        try:
            logger.info(f"POST {url}")
            response = self.client.post(url, data=data, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error for {url}: {e}")
            raise
    
    def close(self):
        """Close HTTP client."""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
