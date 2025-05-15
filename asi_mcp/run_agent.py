#!/usr/bin/env python3
"""
Run MCP Client Agent

This script starts the MCP Client Agent and keeps it running.
"""

import logging
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Use direct import
from agent import MCPClientAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting MCP Client Agent with Chat Protocol support...")
    
    # Create and start the agent with a specific seed phrase
    agent = MCPClientAgent(
        name="mcp_client_agent",
        seed="jjjjjjjqwkjernqwjkhbhbhblfnqwejfbnwehfbverhjgv",
        port=8000
    )
    
    agent_address = agent.agent.address
    logger.info("=" * 50)
    logger.info(f"AGENT ADDRESS: {agent_address}")
    logger.info("=" * 50)
    logger.info("Use this address in the test client when prompted.")
    logger.info("You can interact with this agent using both:")
    logger.info("1. Direct MCP commands (!connect, !list, etc.)")
    logger.info("2. Chat protocol (natural language commands)")
    
    try:
        # This will block until the agent is stopped
        agent.start()
    except KeyboardInterrupt:
        logger.info("Stopping MCP Client Agent...")
        agent.stop()
        logger.info("MCP Client Agent stopped")