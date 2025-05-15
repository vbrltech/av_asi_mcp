#!/usr/bin/env python3
"""
Test Client for Hugging Face Hub MCP Client Agent

This script creates a test client that connects to the Hugging Face Hub MCP Client Agent
using uagents and mailbox, and interacts with it using the chat protocol.
It specifically tests:
1. Connection to the hardcoded MCP server URL
2. Basic command functionality
3. URL override protection
"""

import asyncio
import logging
import uuid
import sys
import os
from datetime import datetime
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent, ChatAcknowledgement, chat_protocol_spec

# Add the parent directory to the Python path so we can import the hardcoded URL
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hugging_face_hub.mcp_client import HUGGINGFACE_MCP_SERVER_URL

# Create the chat protocol instance
chat_proto = Protocol(spec=chat_protocol_spec)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
CLIENT_NAME = "huggingface_test_client"
CLIENT_SEED = "hujjbkbhkbhipbvighvghvhgd_phrase_for_stable_address"
CLIENT_PORT = 8002  # Use a different port than the agent

# Hugging Face Hub MCP Client Agent address - this is the address of the running agent
HF_CLIENT_AGENT_ADDRESS = "agent1qvw9m67nvww0u0csvgqswq9u66a8qxlw9eplthr7xzhyv2xxagglc788ct3"

# Different URL to test URL override protection
DIFFERENT_URL = "https://example.com"

# Initialize Agent
agent = Agent(
    name=CLIENT_NAME,
    seed=CLIENT_SEED,
    port=CLIENT_PORT,
    mailbox=True
)

print(f"Hugging Face Hub Test Client starting. Address: {agent.address}")
print(f"Will send requests to Hugging Face Hub MCP Client Agent at: {HF_CLIENT_AGENT_ADDRESS}")
print(f"Hardcoded MCP server URL: {HUGGINGFACE_MCP_SERVER_URL}")

@agent.on_event("startup")
async def startup(ctx: Context):
    """Send test commands on startup."""
    ctx.logger.info("Hugging Face Hub Test Client started")
    
    # Wait a bit for the mailbox connection to establish
    await asyncio.sleep(5)
    
    # Test 1: Check status and verify connection to hardcoded URL
    ctx.logger.info("\n=== Test 1: Verify connection to hardcoded URL ===")
    await send_command(ctx, "status")
    await asyncio.sleep(3)
    
    # Test 2: List available tools to verify communication
    ctx.logger.info("\n=== Test 2: List available tools ===")
    await send_command(ctx, "list tools")
    await asyncio.sleep(3)
    
    # Test 3: Try to connect to a different URL (should be ignored)
    ctx.logger.info("\n=== Test 3: Test URL override protection ===")
    await send_command(ctx, f"connect to {DIFFERENT_URL}")
    await asyncio.sleep(3)
    
    # Verify we're still using the hardcoded URL
    await send_command(ctx, "status")
    await asyncio.sleep(3)
    
    # Test 4: Try a basic tool call
    ctx.logger.info("\n=== Test 4: Test basic tool call ===")
    await send_command(ctx, "help")
    await asyncio.sleep(3)
    
    # Try calling a specific tool (adjust based on available tools)
    await send_command(ctx, 'call search-models {"query": "bert", "limit": 3}')
    await asyncio.sleep(5)
    
    ctx.logger.info("Test sequence completed")

async def send_command(ctx: Context, command: str):
    """Send a chat command to the Hugging Face Hub MCP Client Agent."""
    ctx.logger.info(f"Sending command: {command}")
    
    chat_msg = ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid.uuid4(),
        content=[TextContent(type="text", text=command)]
    )
    
    try:
        await ctx.send(HF_CLIENT_AGENT_ADDRESS, chat_msg)
        ctx.logger.info("Command sent successfully")
    except Exception as e:
        ctx.logger.error(f"Error sending command: {e}")

@chat_proto.on_message(ChatMessage)
async def handle_chat_response(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages from the Hugging Face Hub MCP Client Agent."""
    ctx.logger.info(f"Received chat message from {sender}:")
    
    for item in msg.content:
        if isinstance(item, TextContent):
            ctx.logger.info(f"Response text: {item.text}")
            
            # Check for hardcoded URL in the response
            if HUGGINGFACE_MCP_SERVER_URL in item.text:
                ctx.logger.info(f"✅ Response contains hardcoded URL: {HUGGINGFACE_MCP_SERVER_URL}")
            
            # Check for different URL in the response
            if DIFFERENT_URL in item.text:
                ctx.logger.info(f"⚠️ Response contains different URL: {DIFFERENT_URL}")
        else:
            ctx.logger.info(f"Received content of type: {type(item)}")
    
    # Send acknowledgement
    try:
        await ctx.send(sender, ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        ))
    except Exception as e:
        ctx.logger.error(f"Error sending acknowledgement: {e}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements from the Hugging Face Hub MCP Client Agent."""
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

# Include the chat protocol
agent.include(chat_proto)

if __name__ == "__main__":
    # Ensure the agent has funds for network operations
    fund_agent_if_low(agent.wallet.address())
    
    # Run the agent
    agent.run()