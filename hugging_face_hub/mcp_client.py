"""
MCP Client - Wrapper for fastmcp Client

This module contains the MCPClient class that wraps the fastmcp Client class,
handles communication with the Hugging Face Hub MCP server, and manages tool calls and responses.
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Any, Union

# Import fastmcp Client and SSETransport
try:
    from fastmcp import Client
    from fastmcp.client.transports import SSETransport
except ImportError:
    raise ImportError("fastmcp package is required. Install it with 'pip install fastmcp'")

# Import schema utilities
from schema_utils import get_schema_from_tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Hardcoded Hugging Face Hub MCP server URL
HUGGINGFACE_MCP_SERVER_URL = "httpmachine.app"


class MCPClient:
    """Wrapper for fastmcp Client to handle communication with the Hugging Face Hub MCP server."""
    
    def __init__(self):
        """Initialize the MCP client."""
        self.client = None
        self.connected = False
        self.server_url = None
        self.tools = []
    
    async def connect(self, url: str = None, token: Optional[str] = None) -> bool:
        """
        Connect to the Hugging Face Hub MCP server.
        
        Args:
            url: Ignored - the hardcoded Hugging Face Hub MCP server URL is always used
            token: Optional authentication token
            
        Returns:
            True if connection was successful, False otherwise
        """
        try:
            # Always use the hardcoded URL
            actual_url = HUGGINGFACE_MCP_SERVER_URL
            
            logger.info(f"Connecting to Hugging Face Hub MCP server at {actual_url}")
            
            # Use SSETransport explicitly for SSE connections
            transport = SSETransport(actual_url)
            self.client = Client(transport)
            
            # Store the URL for later use
            self.server_url = actual_url
            
            # Initialize the client using the async context manager
            await self.client.__aenter__()
            
            # Test the connection by listing tools
            tools = await self.client.list_tools()
            self.tools = tools
            
            self.connected = True
            logger.info(f"Connected to Hugging Face Hub MCP server at {actual_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Hugging Face Hub MCP server at {HUGGINGFACE_MCP_SERVER_URL}: {e}")
            if hasattr(e, '__dict__'):
                logger.error(f"Error details: {e.__dict__}")
            self.client = None
            self.connected = False
            self.server_url = None
            return False
    
    async def disconnect(self) -> bool:
        """
        Disconnect from the MCP server.
        
        Returns:
            True if disconnection was successful, False otherwise
        """
        if not self.connected or not self.client:
            logger.warning("Not connected to the Hugging Face Hub MCP server")
            return True
        
        try:
            # Close the client connection using the async context manager
            await self.client.__aexit__(None, None, None)
            
            self.client = None
            self.connected = False
            logger.info(f"Disconnected from Hugging Face Hub MCP server at {self.server_url}")
            self.server_url = None
            return True
        except Exception as e:
            logger.error(f"Failed to disconnect from Hugging Face Hub MCP server: {e}")
            return False
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available tools on the connected MCP server.
        
        Returns:
            A list of available tools
        """
        if not self.connected or not self.client:
            logger.warning("Not connected to the Hugging Face Hub MCP server")
            return []
        
        try:
            tools = await self.client.list_tools()
            self.tools = tools
            tool_names = [tool.name for tool in tools if hasattr(tool, 'name')]
            logger.info(f"Available tools: {', '.join(tool_names)}")
            return tools
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the connected MCP server.
        
        Args:
            tool_name: The name of the tool to call
            args: The arguments to pass to the tool
            
        Returns:
            The result of the tool call
        """
        if not self.connected or not self.client:
            raise ConnectionError("Not connected to the Hugging Face Hub MCP server")
        
        try:
            logger.info(f"Calling tool '{tool_name}' with arguments: {args}")
            result = await self.client.call_tool(tool_name, args)
            return result
        except Exception as e:
            logger.error(f"Failed to call tool {tool_name}: {e}")
            if hasattr(e, '__dict__'):
                logger.error(f"Error details: {e.__dict__}")
            raise
    
    async def get_schema(self, tool_name: str) -> Dict[str, Any]:
        """
        Get the schema for a tool.
        
        Args:
            tool_name: The name of the tool
            
        Returns:
            The schema for the tool
        """
        if not self.connected or not self.client:
            raise ConnectionError("Not connected to the Hugging Face Hub MCP server")
        
        try:
            tools = await self.list_tools()
            for tool in tools:
                if hasattr(tool, 'name') and tool.name == tool_name:
                    # Use the schema utility function to extract schema
                    return get_schema_from_tool(tool, tool_name)
            
            raise ValueError(f"Tool {tool_name} not found")
        except Exception as e:
            logger.error(f"Failed to get schema for tool {tool_name}: {e}")
            raise
    
    def is_connected(self) -> bool:
        """
        Check if connected to the Hugging Face Hub MCP server.
        
        Returns:
            True if connected, False otherwise
        """
        return self.connected and self.client is not None
    
    def get_server_url(self) -> Optional[str]:
        """
        Get the URL of the connected MCP server.
        
        Returns:
            The URL of the connected MCP server, or None if not connected
        """
        return self.server_url if self.connected else None