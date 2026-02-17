"""
Orchestrator that coordinates all agents.
"""

import logging
import asyncio
from typing import Dict, Any
from backend.models import PredictionRequest
from agents import CrawlerAgent, PreprocessingAgent, MLExecutionAgent
from utils import InstructionLoader, CacheManager

logger = logging.getLogger(__name__)


class PredictionOrchestrator:
    """
    Coordinates the execution of all agents for a prediction.
    
    Pipeline:
    1. Load instructions for model type
    2. Execute 3 crawler agents in parallel
    3. Preprocess data
    4. Generate prediction with ML agent
    5. Return results
    """
    
    def __init__(self):
        """Initialize orchestrator."""
        self.instruction_loader = InstructionLoader()
        self.cache_manager = CacheManager()
    
    async def execute(self, request: PredictionRequest) -> Dict[str, Any]:
        """
        Execute full prediction pipeline.
        
        Args:
            request: Prediction request
            
        Returns:
            Prediction results dictionary
        """
        logger.info(f"Orchestrating prediction for {request.category}/{request.type}")
        
        # Build model type identifier
        model_type = f"{request.category}_{request.type}"
        
        # Convert request to dict for agents
        user_input = request.model_dump(exclude_none=True)
        
        try:
            # Step 1: Load instructions
            logger.info("Loading instructions...")
            instructions = self.instruction_loader.load(model_type)
            crawler_configs = self.instruction_loader.get_crawler_configs(model_type)
            feature_config = self.instruction_loader.get_feature_config(model_type)
            
        except FileNotFoundError:
            logger.warning(f"Instructions not found for {model_type}, using placeholder")
            return self._placeholder_response()
        
        # Step 2: Execute crawlers in parallel
        logger.info("Executing crawler agents...")
        crawler_results = await self._execute_crawlers_parallel(crawler_configs, user_input)
        
        # Step 3: Preprocess data
        logger.info("Preprocessing data...")
        preprocessing_agent = PreprocessingAgent(feature_config)
        features = preprocessing_agent.process(crawler_results, user_input)
        
        # Step 4: Generate prediction
        logger.info("Generating prediction...")
        ml_agent = MLExecutionAgent(model_type)
        result = ml_agent.predict(features)
        
        return result
    
    async def _execute_crawlers_parallel(self, crawler_configs: list, 
                                        user_input: Dict[str, Any]) -> list:
        """
        Execute 3 crawler agents in parallel.
        
        Args:
            crawler_configs: List of 3 crawler configurations
            user_input: User input parameters
            
        Returns:
            List of results from 3 crawlers
        """
        async def run_crawler(config):
            """Run single crawler in executor."""
            loop = asyncio.get_event_loop()
            crawler = CrawlerAgent(config, self.cache_manager)
            return await loop.run_in_executor(None, crawler.execute, user_input)
        
        # Execute all 3 crawlers simultaneously
        tasks = [run_crawler(config) for config in crawler_configs]
        results = await asyncio.gather(*tasks)
        
        return results
    
    def _placeholder_response(self) -> Dict[str, Any]:
        """Return placeholder response when model not available."""
        return {
            "prediction": 0.0,
            "confidence_low": 0.0,
            "confidence_high": 0.0,
            "shap_values": {},
            "explanation": "Model training in progress. This is a placeholder response.",
            "status": "placeholder",
            "warnings": ["Model not yet trained - placeholder response provided"]
        }
