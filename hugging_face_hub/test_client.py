#!/usr/bin/env python3
"""
Test script for the Hugging Face Hub MCP Client

This script tests the Hugging Face Hub MCP Client to verify:
1. It connects to the hardcoded MCP server URL automatically
2. It can communicate with the server
3. Any attempt to connect to a different URL is ignored
"""

import asyncio
import logging
from mcp_client import MCPClient, HUGGINGFACE_MCP_SERVER_URL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_client():
    """Test the Hugging Face Hub MCP Client."""
    client = MCPClient()
    
    # Test 1: Connect with default URL (should use hardcoded URL)
    logger.info("Test 1: Connecting with default URL...")
    connected = await client.connect()
    if connected:
        logger.info(f"✅ Successfully connected to server at: {client.get_server_url()}")
        logger.info(f"✅ Hardcoded URL: {HUGGINGFACE_MCP_SERVER_URL}")
        logger.info(f"✅ URLs match: {client.get_server_url() == HUGGINGFACE_MCP_SERVER_URL}")
    else:
        logger.error("❌ Failed to connect with default URL")
    
    # Test 2: List available tools to verify communication
    if connected:
        logger.info("\nTest 2: Listing available tools...")
        tools = await client.list_tools()
        if tools:
            tool_names = [tool.name for tool in tools if hasattr(tool, 'name')]
            logger.info(f"✅ Successfully listed tools: {', '.join(tool_names)}")
        else:
            logger.error("❌ Failed to list tools or no tools available")
    
    # Test 3: Try to connect with a different URL (should still use hardcoded URL)
    logger.info("\nTest 3: Connecting with a different URL...")
    await client.disconnect()
    different_url = "https://example.com"
    connected = await client.connect(url=different_url)
    if connected:
        logger.info(f"✅ Connected to server at: {client.get_server_url()}")
        logger.info(f"✅ Attempted URL: {different_url}")
        logger.info(f"✅ Hardcoded URL: {HUGGINGFACE_MCP_SERVER_URL}")
        logger.info(f"✅ Using hardcoded URL instead of provided URL: {client.get_server_url() != different_url and client.get_server_url() == HUGGINGFACE_MCP_SERVER_URL}")
    else:
        logger.error("❌ Failed to connect with different URL")
    
    # Clean up
    await client.disconnect()
    logger.info("\nTests completed.")

if __name__ == "__main__":
    asyncio.run(test_client())