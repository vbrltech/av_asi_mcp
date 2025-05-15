# ASI MCP Client Agent

[![domain:mcp-client](https://img.shields.io/badge/domain-mcp--client-blue?style=flat)](.)
[![tech:python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![tech:uagents](https://img.shields.io/badge/uAgents-000000?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDBDNS4zNzMgMCAwIDUuMzczIDAgMTJDNy4xNTMgMTIgMTIgNy4xNTMgMTIgMFoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0xMiAyNEMxOC42MjcgMjQgMjQgMTguNjI3IDI0IDEyQzE2Ljg0NyAxMiAxMiAxNi4xNTMgMTIgMjRaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)](https://fetch.ai/uagents)
[![tech:fastmcp](https://img.shields.io/badge/fastmcp-007ACC?style=flat)](https://github.com/fetchai/fastmcp)
[![tech:sse-transport](https://img.shields.io/badge/SSE--transport-FF6600?style=flat)](.)
[![link to source code](https://img.shields.io/badge/source-asi__mcp-green?style=flat)](./asi_mcp/)

This agent acts as a client for Model Context Protocol (MCP) servers, allowing users to connect to any MCP server via SSE transport and interact with available tools through a chat interface.

Interaction with this agent is supported via both the standard chat_protocol and direct commands. You can send natural language commands or structured commands to connect to MCP servers and call tools.

IMPORTANT: The agent supports both structured commands and natural language commands via chat. For chat commands, your message must start with one of the phrases listed in the "Sample Chat Commands" section below (e.g., `connect to`, `list tools`, `call`). The agent will translate these into the appropriate structured commands.

Internally, the agent maintains connection state with MCP servers, handles tool calls, and formats responses in a readable way. It's designed to work with any MCP server that supports the SSE transport protocol.

## Example Chat Interaction

### Example Input (Chat Message)
```python
# Client sends a ChatMessage
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent

# Example chat request
chat_message = ChatMessage(
    content=[
        TextContent(text="connect to https://cloud.activepieces.com/api/v1/mcp/RerVk5mI66ZTiq9Xc8aIu/sse")
    ]
)
# Client sends this message to the MCP Client Agent's address
```

### Example Output (Chat Response)
The agent acknowledges the chat message and then sends a confirmation of the connection.

```python
# Agent sends a ChatMessage response
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent

# Example response
response_message = ChatMessage(
    content=[
        TextContent(text="✅ Connected to https://cloud.activepieces.com/api/v1/mcp/RerVk5mI66ZTiq9Xc8aIu/sse\n\nFound 2 available tools. Use `list` to see them.")
    ]
)
# Agent sends this message back to the client
```

### Example Tool Call via Chat

```python
# Client sends a ChatMessage to call a tool
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent

# Example tool call request
chat_message = ChatMessage(
    content=[
        TextContent(text="call open-router-ask-lmm {\"prompt\": \"Hello, how are you?\"}")
    ]
)
# Client sends this message to the MCP Client Agent's address
```

### Example Tool Call Response

```python
# Agent sends the tool call result via ChatMessage
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent

# Example tool call response
response_message = ChatMessage(
    content=[
        TextContent(text="✅ Tool call successful:\n\n```\n[type='text' text='✅ Successfully executed Ask LLM\n\nAsk any model supported by Open Router.\n\n```json\n{\n  \"success\": true,\n  \"input\": {\n    \"model\": \"pygmalionai/mythalion-13b\",\n    \"prompt\": \"Hello, how are you?\",\n    \"auth\": \"**REDACTED**\"\n  },\n  \"output\": \"My name is Laura. Thanks for having me here. I am creative, fun-loving and working as a freelance writer. I\\'m extremely excited to share my experience and knowledge with you. Most of my articles are related to writing, business, and education. I am an experienced writer and I promise to share valuable information with you. Kindly connect with me for your writing or editing needs.\"\n}\n```' annotations=None]\n```")
    ]
)
# Agent sends this message back to the client
```

## Sample Chat Commands

IMPORTANT: For chat protocol interactions, your message should start with one of the phrases below (case-insensitive).

Here are some examples of commands you can send to the agent via chat:

### Connection Management:
- `connect to https://example.com/mcp/sse`
- `connect to https://example.com/mcp/sse with token YOUR_TOKEN`
- `disconnect`

### Tool Discovery and Status:
- `list tools`
- `status`
- `help`
- `help connect`

### Tool Calling:
- `call tool_name {"param": "value"}`
- `schema tool_name`

## Supported Structured Commands

The agent also supports direct structured commands:

- `connect [url] [--token TOKEN] [--token-env-var VAR_NAME]`
- `disconnect`
- `list`
- `call [tool_name] [json_args]`
- `shorthand [tool_name] [arg1=value1] [arg2=value2] ...`
- `schema [tool_name]`
- `status`
- `help`

## Usage Example (Chat Client)

Copy and paste the following code into a new Python file (e.g., `chat_client_example.py`) for an example of how to interact with this agent using chat.

```python
import asyncio
import logging
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import chat_proto, ChatMessage, TextContent, ChatAcknowledgement

# Configuration
CLIENT_NAME = "mcp_chat_client"
CLIENT_SEED = "mcp_chat_client_seed"

# MCP Client Agent address - **MUST MATCH THE RUNNING AGENT**
MCP_CLIENT_AGENT_ADDRESS = "agent1q....." # Replace with actual agent address

# Logging
logging.basicConfig(level=logging.INFO)

# Initialize Agent
agent = Agent(
    name=CLIENT_NAME,
    seed=CLIENT_SEED,
    port=8001, # Use a different port
    mailbox=True
)

print(f"Chat Client Example starting. Address: {agent.address}")
print(f"Will send request to: {MCP_CLIENT_AGENT_ADDRESS}")

@agent.on_event("startup")
async def send_chat_request(ctx: Context):
    """Send a chat message request on startup."""
    command = "connect to https://cloud.activepieces.com/api/v1/mcp/RerVk5mI66ZTiq9Xc8aIu/sse"
    ctx.logger.info(f"Sending chat request: {command}")
    
    chat_msg = ChatMessage(content=[TextContent(text=command)])
    
    try:
        await ctx.send(MCP_CLIENT_AGENT_ADDRESS, chat_msg)
        ctx.logger.info("Chat request sent successfully.")
    except Exception as e:
        ctx.logger.error(f"Error sending chat request: {e}")

@chat_proto.on_message(ChatMessage)
async def handle_chat_response(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages from the server."""
    ctx.logger.info(f"Received chat message from {sender}:")
    for item in msg.content:
        if isinstance(item, TextContent):
            ctx.logger.info(f"  -> Text: '{item.text}'")
        else:
            ctx.logger.info(f"  -> Received content of type: {type(item)}")

    # Acknowledge receipt
    try:
        await ctx.send(sender, ChatAcknowledgement(acknowledged_msg_id=msg.msg_id))
    except Exception as e:
        ctx.logger.error(f"Error sending chat acknowledgement: {e}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements from the server."""
    ctx.logger.info(f"Received chat ACK from {sender} for message {msg.acknowledged_msg_id}")

# Include the protocol
agent.include(chat_proto)

if __name__ == "__main__":
    # Ensure the agent has funds if needed for mailbox registration etc.
    fund_agent_if_low(agent.wallet.address())
    
    # Run the agent
    agent.run()
```

## Running the Agent

1. Clone the repository (if you haven't already):
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r asi_mcp/requirements.txt
   ```

3. Run the agent:
   ```bash
   python asi_mcp/run_agent.py
   ```

4. Note the agent address printed in the logs.

## Running the Example Chat Client

1. Save the "Usage Example (Chat Client)" code above as `chat_client_example.py`.
2. Replace Placeholder: Update the `MCP_CLIENT_AGENT_ADDRESS` variable in `chat_client_example.py` with the actual address of your running MCP Client Agent.
3. Run the client:
   ```bash
   python chat_client_example.py
   ```

The client will send a chat request on startup and log the response received from the main agent.

## Architecture

The MCP Client Agent consists of the following components:

1. **Agent Core**: Main agent class that initializes the uagents framework
2. **Chat Protocol Handler**: Processes incoming chat messages
3. **Command Parser**: Parses structured commands from messages
4. **Session Manager**: Maintains connection state with MCP servers
5. **MCP Client**: Wraps the fastmcp Client class
6. **Result Formatter**: Formats MCP responses into readable chat messages
7. **Schema Utilities**: Centralizes schema extraction, validation, and parameter handling
8. **Parameter Validator**: Automatically validates and fills tool parameters

## Parameter Validation and Auto-filling

The agent now includes intelligent parameter handling for tool calls:

1. **Schema-based Validation**: When calling a tool, the agent automatically validates the provided parameters against the tool's schema.

2. **Required Parameter Detection**: The agent identifies which parameters are required and verifies they are provided.

3. **Default Value Auto-filling**: For optional parameters with default values defined in the schema, the agent automatically fills them if not provided by the user.

4. **Helpful Error Messages**: When parameter validation fails, the agent provides detailed error messages with:
   - List of missing required parameters
   - Parameter types and descriptions
   - Example usage with the correct format

Example error message:
```
❌ Parameter validation error for tool 'open-router-ask-lmm':
Missing required parameters: prompt

Required parameters:
- `prompt`: string - The text prompt to send to the model

Example usage:
call open-router-ask-lmm {
  "prompt": "example_string"
}
```

This feature makes the agent more user-friendly by reducing errors and providing clear guidance when parameters are missing or incorrect.

## Schema Utilities

The agent includes a dedicated schema handling system that centralizes schema-related operations:

1. **Robust Schema Extraction**: The `schema_utils` module provides functions to extract schema information from tool objects, handling various schema formats and attribute names.

2. **Method/Callable Schema Support**: The agent can now handle tools that provide schemas as callable methods rather than direct dictionaries, improving compatibility with a wider range of MCP servers.

3. **Schema Validation**: Utility functions validate schema structures to ensure they conform to expected formats before processing.

4. **Centralized Parameter Extraction**: The utilities provide standardized methods for extracting required and optional parameters from schemas.

5. **Error Resilience**: The schema handling system includes comprehensive error handling to gracefully manage unexpected schema formats or missing information.

These utilities make the agent more robust when interacting with different MCP servers that might implement the schema specification in slightly different ways. The modular design also makes it easier to extend or modify schema handling behavior in the future.

## Schema Command

The agent now supports a dedicated `schema` command that allows clients to request detailed schema information for any tool:

```
schema [tool_name]
```

This command returns comprehensive information about a tool's schema, including:

1. **Parameter Details**: All parameters with their types, descriptions, and whether they're required or optional
2. **Default Values**: Default values for optional parameters
3. **Constraints**: Any constraints like minimum/maximum values, allowed formats, or enum values
4. **Example Usage**: A ready-to-use example showing how to call the tool with required parameters
5. **Raw Schema**: The complete JSON schema for advanced users

Example output:

```
📝 Schema for tool 'stability-ai-text-to-image':

**Parameters**:

- **`prompt`** (required): `string`
  The text prompt to generate an image from

- **`negative_prompt`** (optional): `string`
  Text to exclude from the image
  Default: ""

- **`width`** (optional): `integer`
  Width of the generated image
  Minimum: 512
  Maximum: 1024
  Default: `512`

- **`height`** (optional): `integer`
  Height of the generated image
  Minimum: 512
  Maximum: 1024
  Default: `512`

**Example Usage**:

call stability-ai-text-to-image {
  "prompt": "example_string",
  "negative_prompt": ""
}

**Raw Schema**:
{
  "type": "object",
  "properties": {
    "prompt": {
      "type": "string",
      "description": "The text prompt to generate an image from"
    },
    ...
  },
  "required": [
    "prompt"
  ]
}
```

This feature makes it easier for clients to understand how to use tools correctly, explore available options, and see the full schema details.

### Enhanced Schema Formatting

The schema command now provides improved formatting for better readability:

- **Organized Parameters**: Parameters are sorted with required parameters first
- **Parameter Counts**: Shows counts of required and optional parameters
- **Comprehensive Constraints**: Displays all constraints in a clear format
- **Smart Example Generation**: Creates realistic examples based on parameter types and formats
- **Multiple Command Examples**: Shows both natural language and structured command examples
- **Large Schema Handling**: Truncates large schemas to prevent overwhelming output

### Robust Error Handling

The schema command includes comprehensive error handling for edge cases:

- **Invalid Schemas**: Gracefully handles missing or malformed schemas
- **Callable Schemas**: Properly handles schemas provided as methods
- **Type Conversion**: Attempts to convert non-dictionary objects to dictionaries
- **Detailed Logging**: Provides informative error messages for troubleshooting

### Testing the Schema Command

The repository includes dedicated test clients for verifying the schema command functionality:

- **Basic Test Client** (`test_schema_client.py`): Tests the natural language schema command
- **Comprehensive Test Client** (`test_schema_comprehensive.py`): Tests both command formats

See `SCHEMA_TESTING.md` for detailed testing instructions.

## Example MCP Servers

You can test the agent with the following MCP server:
- SSE MCP Server: `https://cloud.activepieces.com/api/v1/mcp/RerVk5mI66ZTiq9Xc8aIu/sse`
