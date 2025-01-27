"""
Main assistant implementation.
"""
import logging
from kubewhisper.llm.deepseek import DeepSeekLLM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Assistant:
    """
    Main assistant class.
    """

    def __init__(self):
        """
        Initialize the assistant.
        """
        self.llm = DeepSeekLLM()
        
    async def process_query(self, query: str):
        """
        Process a user query through the LLM.
        
        Args:
            query: The user's question or command
            
        Returns:
            The processed response
        """
        logger.info(f"Processing query: {query}")
        response = await self.llm.ask_question(query)
        logger.info(f"Got response: {response}")
        return response
