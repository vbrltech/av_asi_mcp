#!/usr/bin/env python3
"""
Run the Hugging Face Hub Agent

This script starts the Hugging Face Hub Agent, which connects
to the Hugging Face Hub API server and provides a chat interface for
interacting with the Hugging Face Hub API.
"""

import argparse
import logging
import os
import sys

# Add the parent directory to the Python path so we can import asi_mcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import HuggingFaceHubAgent, HUGGINGFACE_SERVER_URL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Run the Hugging Face Hub Agent."""
    parser = argparse.ArgumentParser(description="Run the Hugging Face Hub Agent")
    parser.add_argument("--name", type=str, default="huggingface_hub_agent",
                        help="Name of the agent")
    parser.add_argument("--seed", type=str, default="ugty",
                        help="Seed for agent identity (if None, a random one will be generated)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port for the agent's HTTP endpoint")
    
    args = parser.parse_args()
    
    logger.info(f"Starting Hugging Face Hub Agent")
    logger.info(f"Server URL: {HUGGINGFACE_SERVER_URL}")
    
    # Create and start the agent
    agent = HuggingFaceHubAgent(
        name=args.name,
        seed=args.seed,
        port=args.port
    )
    
    agent.start()


if __name__ == "__main__":
    main()