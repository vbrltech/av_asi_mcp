"""
Hugging Face Hub Agent - Main agent class

This module contains the main agent class that initializes the uagents framework,
handles chat protocol, and manages startup and shutdown for the Hugging Face Hub client.
"""

import asyncio
import logging
from typing import Dict, Optional, Any, Callable

from uagents import Agent, Context, Protocol, Model

from chat_handler import ChatHandler
from command_parser import CommandParser
from session_manager import SessionManager
from hub_client import HubClient, HUGGINGFACE_SERVER_URL
from result_formatter import ResultFormatter
from chat_proto import chat_proto

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define message models
class ChatMessage(Model):
    """Model for chat messages."""
    content: str
    sender: Optional[str] = None


class ChatResponse(Model):
    """Model for chat responses."""
    content: str
    recipient: Optional[str] = None


class HuggingFaceHubAgent:
    """
    Hugging Face Hub Agent that connects to the Hugging Face Hub API server
    and provides a chat interface for interacting with it.
    """
    
    def __init__(self, name: str = "huggingface_hub_agent", seed: Optional[str] = None, port: int = 8000):
        """
        Initialize the Hugging Face Hub Agent.
        
        Args:
            name: Name of the agent
            seed: Seed for agent identity (if None, a random one will be generated)
            port: Port for the agent's HTTP endpoint
        """
        self.name = name
        self.seed = seed
        self.port = port
        
        # Create the uagents Agent with mailbox enabled
        self.agent = Agent(
            name=name,
            seed=seed,
            port=port,
            mailbox=True,
        )
        
        # Initialize components
        self.result_formatter = ResultFormatter()
        self.hub_client = HubClient()
        self.session_manager = SessionManager(self.hub_client)
        self.command_parser = CommandParser()
        self.chat_handler = ChatHandler(
            command_parser=self.command_parser,
            session_manager=self.session_manager,
            result_formatter=self.result_formatter
        )
        
        # Set up chat protocol
        self.chat_protocol = Protocol("chat")
        
        @self.chat_protocol.on_message(model=ChatMessage)
        async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
            """Handle incoming chat messages."""
            logger.info(f"Received message from {sender}: {msg.content}")
            
            # Process the message
            response = await self.chat_handler.process_message(msg.content, sender)
            
            # Send response
            await ctx.send(sender, ChatResponse(content=response, recipient=sender))
            logger.info(f"Sent response to {sender}")
        
        # Register the protocols with the agent
        self.agent.include(self.chat_protocol)
        
        # Set the agent instance in the chat_proto module and include the protocol
        from chat_proto import set_agent_instance, chat_proto
        set_agent_instance(self)
        self.agent.include(chat_proto, publish_manifest=True)
        
        logger.info(f"Hugging Face Hub Agent initialized. Server URL: {HUGGINGFACE_SERVER_URL}")
    
    async def auto_connect(self):
        """Automatically connect to the Hugging Face Hub API server."""
        logger.info(f"Automatically connecting to Hugging Face Hub API server at {HUGGINGFACE_SERVER_URL}")
        result = await self.session_manager.connect()
        if result.get("success"):
            logger.info(f"Successfully auto-connected to Hugging Face Hub API server")
        else:
            logger.warning(f"Failed to auto-connect to Hugging Face Hub API server: {result.get('message')}")
        return result

    def start(self):
        """Start the agent."""
        logger.info(f"Starting Hugging Face Hub Agent on port {self.port}")
        
        # Create a background task for auto-connection
        # We'll use a separate thread to run the asyncio event loop for auto-connection
        import threading
        
        def run_auto_connect():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.auto_connect())
            loop.close()
        
        # Start the auto-connect thread before running the agent
        threading.Thread(target=run_auto_connect).start()
        
        # Run the agent
        self.agent.run()
    
    def stop(self):
        """Stop the agent."""
        logger.info("Stopping Hugging Face Hub Agent")
        # Cleanup resources
        asyncio.create_task(self.session_manager.disconnect_all())
    
    async def process_message(self, message: str, sender: Optional[str] = None) -> str:
        """
        Process a chat message and return a response.
        
        This method can be used directly without going through the agent protocol,
        which is useful for testing or direct integration.
        
        Args:
            message: The message content
            sender: Optional sender identifier
            
        Returns:
            Response message
        """
        return await self.chat_handler.process_message(message, sender)


if __name__ == "__main__":
    # Example usage
    agent = HuggingFaceHubAgent()
    agent.start()