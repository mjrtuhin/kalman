"""
Generic crawler agent that adapts behavior based on JSON instructions.
"""

import logging
from typing import Dict, Any, Optional
from utils.cache_manager import CacheManager
from utils.api_client import APIClient

logger = logging.getLogger(__name__)


class CrawlerAgent:
    """
    Generic crawler that fetches data based on instruction configuration.
    
    Key Features:
    - Cache-first strategy
    - Automatic retry logic
    - Schema validation
    - Error handling with fallbacks
    """
    
    def __init__(self, config: Dict[str, Any], cache_manager: Optional[CacheManager] = None):
        """
        Initialize crawler agent.
        
        Args:
            config: Crawler configuration from instruction JSON
            cache_manager: Cache manager instance (creates new if None)
        """
        self.config = config
        self.name = config.get("name", "UnnamedCrawler")
        self.data_sources = config.get("data_sources", [])
        
        # Initialize cache manager
        self.cache = cache_manager or CacheManager()
        
        # Initialize API client
        self.api_client = APIClient()
        
        logger.info(f"Initialized {self.name}")
    
    def execute(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute crawler - fetch data from all configured sources.
        
        Args:
            user_input: User input parameters (postcode, business type, etc.)
            
        Returns:
            Dictionary with data from all sources
        """
        logger.info(f"Executing {self.name}")
        
        results = {
            "crawler_name": self.name,
            "sources": {}
        }
        
        for source_config in self.data_sources:
            source_name = source_config.get("name")
            
            try:
                data = self._fetch_source(source_config, user_input)
                results["sources"][source_name] = data
                logger.info(f"✓ Fetched data from {source_name}")
                
            except Exception as e:
                logger.error(f"✗ Failed to fetch {source_name}: {e}")
                results["sources"][source_name] = {
                    "error": str(e),
                    "status": "failed"
                }
        
        return results
    
    def _fetch_source(self, source_config: Dict[str, Any], 
                     user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch data from a single source.
        
        Args:
            source_config: Source configuration
            user_input: User input parameters
            
        Returns:
            Data from source
        """
        source_name = source_config.get("name")
        source_type = source_config.get("type")
        ttl_days = source_config.get("cache_ttl_days", 30)
        
        # Generate cache key
        cache_key = self._generate_cache_key(source_config, user_input)
        
        # Check cache first
        cached_data = self.cache.get(source_name, cache_key, ttl_days)
        if cached_data:
            logger.info(f"Cache hit for {source_name}")
            return cached_data
        
        # Cache miss - fetch from source
        logger.info(f"Cache miss for {source_name}, fetching...")
        
        if source_type == "rest_api":
            data = self._fetch_rest_api(source_config, user_input)
        elif source_type == "bulk_csv":
            data = self._fetch_bulk_csv(source_config, user_input)
        elif source_type == "csv_static":
            data = self._fetch_csv_static(source_config, user_input)
        else:
            raise ValueError(f"Unknown source type: {source_type}")
        
        # Cache the result
        self.cache.set(source_name, cache_key, data, ttl_days)
        
        return data
    
    def _fetch_rest_api(self, source_config: Dict[str, Any], 
                       user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch data from REST API."""
        url_template = source_config.get("url")
        params_mapping = source_config.get("params_mapping", {})
        
        # Build URL with user input
        url = self._interpolate_template(url_template, user_input)
        
        # Build query parameters
        params = {}
        for key, value_template in params_mapping.items():
            params[key] = self._interpolate_template(value_template, user_input)
        
        # Make API call
        response = self.api_client.get(url, params=params)
        
        return {
            "status": "success",
            "data": response,
            "source": source_config.get("name")
        }
    
    def _fetch_bulk_csv(self, source_config: Dict[str, Any], 
                       user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch data from bulk CSV file."""
        # Placeholder - will implement in training pipeline
        return {
            "status": "not_implemented",
            "message": "Bulk CSV fetching implemented in training pipeline",
            "source": source_config.get("name")
        }
    
    def _fetch_csv_static(self, source_config: Dict[str, Any], 
                         user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch data from static CSV file."""
        # Placeholder - will implement in training pipeline
        return {
            "status": "not_implemented",
            "message": "Static CSV fetching implemented in training pipeline",
            "source": source_config.get("name")
        }
    
    def _generate_cache_key(self, source_config: Dict[str, Any], 
                           user_input: Dict[str, Any]) -> str:
        """Generate unique cache key from source config and user input."""
        source_name = source_config.get("name", "unknown")
        
        # Create key from relevant user inputs
        key_parts = [source_name]
        
        # Add user input values that affect the query
        if "postcode" in user_input:
            key_parts.append(user_input["postcode"])
        if "business_type" in user_input:
            key_parts.append(user_input["business_type"])
        
        return "_".join(key_parts)
    
    def _interpolate_template(self, template: str, user_input: Dict[str, Any]) -> str:
        """
        Replace template placeholders with user input values.
        
        Example: "{user_input.postcode}" -> "SW1A 1AA"
        """
        if not isinstance(template, str):
            return template
        
        result = template
        
        # Replace {user_input.key} patterns
        for key, value in user_input.items():
            placeholder = f"{{user_input.{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        
        return result
    
    def __del__(self):
        """Cleanup when agent is destroyed."""
        if hasattr(self, 'api_client'):
            self.api_client.close()
