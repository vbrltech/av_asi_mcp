"""
Hugging Face Hub Client Example

This example demonstrates how to use the Hugging Face Hub MCP Client Agent
to interact with the Hugging Face Hub API through the MCP server.
"""

import asyncio
import logging
from hugging_face_hub.agent import HuggingFaceHubAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    """Run the Hugging Face Hub client example."""
    # Create the agent without starting the uagents server
    agent = HuggingFaceHubAgent()
    
    # Process commands directly
    
    # Connect to the Hugging Face Hub MCP server
    logger.info("Connecting to Hugging Face Hub MCP server...")
    response = await agent.process_message("!connect")
    print(f"\nResponse:\n{response}\n")
    
    # List available tools
    logger.info("Listing available tools...")
    response = await agent.process_message("!list")
    print(f"\nResponse:\n{response}\n")
    
    # Check status
    logger.info("Checking status...")
    response = await agent.process_message("!status")
    print(f"\nResponse:\n{response}\n")
    
    # Search for models using JSON syntax
    logger.info("Searching for models with JSON syntax...")
    response = await agent.process_message('!call search-models {"query": "llama", "limit": 3}')
    print(f"\nResponse:\n{response}\n")
    
    # Search for models using shorthand syntax
    logger.info("Searching for models with shorthand syntax...")
    response = await agent.process_message('!shorthand search-models query="stable-diffusion" limit=3')
    print(f"\nResponse:\n{response}\n")
    
    # Get model info
    logger.info("Getting model info...")
    response = await agent.process_message('!shorthand get-model-info model_id="meta-llama/Llama-3-8B-Instruct"')
    print(f"\nResponse:\n{response}\n")
    
    # Search for datasets
    logger.info("Searching for datasets...")
    response = await agent.process_message('!shorthand search-datasets query="squad" limit=3')
    print(f"\nResponse:\n{response}\n")
    
    # Get daily papers
    logger.info("Getting daily papers...")
    response = await agent.process_message('!call get-daily-papers {}')
    print(f"\nResponse:\n{response}\n")
    
    # Disconnect
    logger.info("Disconnecting from Hugging Face Hub MCP server...")
    response = await agent.process_message("!disconnect")
    print(f"\nResponse:\n{response}\n")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())