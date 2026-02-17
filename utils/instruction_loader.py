"""
Loads and parses instruction JSON files for crawler agents.
"""

import json
from typing import Dict, List
from pathlib import Path


class InstructionLoader:
    """Loads instruction JSON files for different model types."""
    
    def __init__(self, config_dir: str = "config/instructions"):
        """
        Initialize instruction loader.
        
        Args:
            config_dir: Directory containing instruction JSON files
        """
        self.config_dir = Path(config_dir)
    
    def load(self, model_type: str) -> Dict:
        """
        Load instruction JSON for given model type.
        
        Args:
            model_type: Model identifier (e.g., "house_general", "business_restaurant")
            
        Returns:
            Instruction configuration dict
            
        Raises:
            FileNotFoundError: If instruction file doesn't exist
            ValueError: If required fields missing
        """
        file_path = self.config_dir / f"{model_type}_instructions.json"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Instruction file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            instructions = json.load(f)
        
        # Validate required fields
        required = ["model_type", "crawler_1", "crawler_2", "crawler_3"]
        for field in required:
            if field not in instructions:
                raise ValueError(f"Missing required field '{field}' in {file_path}")
        
        return instructions
    
    def get_crawler_configs(self, model_type: str) -> List[Dict]:
        """
        Extract crawler configurations as list.
        
        Args:
            model_type: Model identifier
            
        Returns:
            List of 3 crawler configuration dicts
        """
        instructions = self.load(model_type)
        return [
            instructions["crawler_1"],
            instructions["crawler_2"],
            instructions["crawler_3"]
        ]
    
    def get_feature_config(self, model_type: str) -> Dict:
        """
        Get feature engineering configuration.
        
        Args:
            model_type: Model identifier
            
        Returns:
            Feature engineering configuration dict
        """
        instructions = self.load(model_type)
        return instructions.get("feature_engineering", {})
