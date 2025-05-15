# Hugging Face Hub Agent

[![domain:huggingface](https://img.shields.io/badge/domain-huggingface-blue?style=flat)](.)
[![tech:python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![tech:uagents](https://img.shields.io/badge/uAgents-000000?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDBDNS4zNzMgMCAwIDUuMzczIDAgMTJDNy4xNTMgMTIgMTIgNy4xNTMgMTIgMFoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0xMiAyNEMxOC42MjcgMjQgMjQgMTguNjI3IDI0IDEyQzE2Ljg0NyAxMiAxMiAxNi4xNTMgMTIgMjRaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)](https://fetch.ai/uagents)
[![link to source code](https://img.shields.io/badge/source-hugging__face__hub-green?style=flat)](./hugging_face_hub/)

This agent allows users to interact with the Hugging Face Hub and access available tools through a chat interface.

Interaction with this agent is supported via both the standard chat_protocol and direct commands. You can send natural language commands or structured commands to call tools.

IMPORTANT: The agent supports both structured commands and natural language commands via chat. For chat commands, your message must start with one of the phrases listed in the "Sample Chat Commands" section below (e.g., `list tools`, `call`). The agent will translate these into the appropriate structured commands.

Internally, the agent handles tool calls and formats responses in a readable way.

## Example Chat Interaction

### Example Input (Chat Message)
```python
# Client sends a ChatMessage
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent

# Example chat request
chat_message = ChatMessage(
    content=[
        TextContent(text="list tools")
    ]
)
# Client sends this message to the Hugging Face Hub Agent's address
```

### Example Output (Chat Response)
The agent acknowledges the chat message and then sends a list of available tools.

```python
# Agent sends a ChatMessage response
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent

# Example response
response_message = ChatMessage(
    content=[
        TextContent(text="📋 Available tools (10):\n\n1. search-models: Search for models on Hugging Face Hub\n2. get-model-info: Get detailed information about a specific model\n3. search-datasets: Search for datasets on Hugging Face Hub\n4. get-dataset-info: Get detailed information about a specific dataset\n5. search-spaces: Search for Spaces on Hugging Face Hub\n6. get-space-info: Get detailed information about a specific Space\n7. get-paper-info: Get information about a specific paper\n8. get-daily-papers: Get the list of daily papers\n9. search-collections: Search for collections on Hugging Face Hub\n10. get-collection-info: Get detailed information about a specific collection\n\nUse `schema [tool_name]` to see details for a specific tool.")
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
        TextContent(text="call search-models {\"query\": \"stable-diffusion\", \"limit\": 5}")
    ]
)
# Client sends this message to the Hugging Face Hub Agent's address
```

### Example Tool Call Response

```python
# Agent sends the tool call result via ChatMessage
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent

# Example tool call response
response_message = ChatMessage(
    content=[
        TextContent(text="✅ Tool call successful:\n\n```\n{\n  \"success\": true,\n  \"models\": [\n    {\n      \"id\": \"stabilityai/stable-diffusion-xl-base-1.0\",\n      \"name\": \"Stable Diffusion XL 1.0\",\n      \"description\": \"SDXL text-to-image model\",\n      \"downloads\": 1250000,\n      \"likes\": 8500\n    },\n    {\n      \"id\": \"runwayml/stable-diffusion-v1-5\",\n      \"name\": \"Stable Diffusion v1.5\",\n      \"description\": \"Stable Diffusion version 1.5 release\",\n      \"downloads\": 2100000,\n      \"likes\": 12000\n    },\n    {\n      \"id\": \"stabilityai/stable-diffusion-2-1\",\n      \"name\": \"Stable Diffusion 2.1\",\n      \"description\": \"Stable Diffusion version 2.1\",\n      \"downloads\": 1800000,\n      \"likes\": 9800\n    },\n    {\n      \"id\": \"CompVis/stable-diffusion-v1-4\",\n      \"name\": \"Stable Diffusion v1.4\",\n      \"description\": \"Original Stable Diffusion release\",\n      \"downloads\": 1500000,\n      \"likes\": 7500\n    },\n    {\n      \"id\": \"stabilityai/stable-diffusion-xl-refiner-1.0\",\n      \"name\": \"SDXL Refiner 1.0\",\n      \"description\": \"SDXL refiner model for enhanced details\",\n      \"downloads\": 980000,\n      \"likes\": 6200\n    }\n  ]\n}\n```")
    ]
)
# Agent sends this message back to the client
```

## Sample Chat Commands

IMPORTANT: For chat protocol interactions, your message should start with one of the phrases below (case-insensitive).

Here are some examples of commands you can send to the agent via chat:

### Tool Discovery and Status:
- `list tools`
- `status`
- `help`

### Tool Calling:
- `call search-models {"query": "stable-diffusion", "limit": 5}`
- `schema search-models`

## Supported Structured Commands

The agent also supports direct structured commands:

- `list`
- `call [tool_name] [json_args]`
- `shorthand [tool_name] [arg1=value1] [arg2=value2] ...`
- `schema [tool_name]`
- `status`
- `help`
- `disconnect`

## Usage Example (Chat Client)

Copy and paste the following code into a new Python file (e.g., `chat_client_example.py`) for an example of how to interact with this agent using chat.

```python
import asyncio
import logging
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import chat_proto, ChatMessage, TextContent, ChatAcknowledgement

# Configuration
CLIENT_NAME = "huggingface_chat_client"
CLIENT_SEED = "huggingface_chat_client_seed"

# Hugging Face Hub Agent address - **MUST MATCH THE RUNNING AGENT**
HF_AGENT_ADDRESS = "agent1q....." # Replace with actual agent address

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
print(f"Will send request to: {HF_AGENT_ADDRESS}")

@agent.on_event("startup")
async def send_chat_request(ctx: Context):
    """Send a chat message request on startup."""
    command = "list tools"
    ctx.logger.info(f"Sending chat request: {command}")
    
    chat_msg = ChatMessage(content=[TextContent(text=command)])
    
    try:
        await ctx.send(HF_AGENT_ADDRESS, chat_msg)
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
   pip install -r hugging_face_hub/requirements.txt
   ```

3. Run the agent:
   ```bash
   python hugging_face_hub/run_agent.py
   ```

4. Note the agent address printed in the logs.

## Running the Example Chat Client

1. Save the "Usage Example (Chat Client)" code above as `chat_client_example.py`.
2. Replace Placeholder: Update the `HF_AGENT_ADDRESS` variable in `chat_client_example.py` with the actual address of your running Hugging Face Hub Agent.
3. Run the client:
   ```bash
   python chat_client_example.py
   ```

The client will send a chat request on startup and log the response received from the main agent.

## Architecture

The Hugging Face Hub Agent consists of the following components:

1. **Agent Core**: Main agent class that initializes the uagents framework
2. **Chat Protocol Handler**: Processes incoming chat messages
3. **Command Parser**: Parses structured commands from messages
4. **Tool Manager**: Manages tool access and execution
5. **Result Formatter**: Formats responses into readable chat messages
6. **Schema Utilities**: Centralizes schema extraction, validation, and parameter handling
7. **Parameter Validator**: Automatically validates and fills tool parameters

## Parameter Validation and Auto-filling

The agent includes intelligent parameter handling for tool calls:

1. **Schema-based Validation**: When calling a tool, the agent automatically validates the provided parameters against the tool's schema.

2. **Required Parameter Detection**: The agent identifies which parameters are required and verifies they are provided.

3. **Default Value Auto-filling**: For optional parameters with default values defined in the schema, the agent automatically fills them if not provided by the user.

4. **Helpful Error Messages**: When parameter validation fails, the agent provides detailed error messages with:
   - List of missing required parameters
   - Parameter types and descriptions
   - Example usage with the correct format

Example error message:
```
❌ Parameter validation error for tool 'search-models':
Missing required parameters: query

Required parameters:
- `query`: string - Search term (e.g., 'bert', 'gpt')

Example usage:
call search-models {
  "query": "example_string"
}
```

This feature makes the agent more user-friendly by reducing errors and providing clear guidance when parameters are missing or incorrect.

## Schema Command

The agent supports a dedicated `schema` command that allows clients to request detailed schema information for any tool:

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
📝 Schema for tool 'search-models':

**Parameters**:

- **`query`** (required): `string`
  Search term (e.g., 'bert', 'gpt')

- **`author`** (optional): `string`
  Filter by author/organization (e.g., 'huggingface', 'google')

- **`tags`** (optional): `string`
  Filter by tags (e.g., 'text-classification', 'translation')

- **`limit`** (optional): `integer`
  Maximum number of results to return
  Default: `10`

**Example Usage**:

call search-models {
  "query": "stable-diffusion",
  "limit": 5
}

**Raw Schema**:
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search term (e.g., 'bert', 'gpt')"
    },
    ...
  },
  "required": [
    "query"
  ]
}
```

## Hugging Face Hub Tools

The Hugging Face Hub Agent provides access to a variety of tools for interacting with different aspects of the Hugging Face ecosystem. This section provides detailed information about each available tool, organized by category.

### Model Tools

#### `search-models`
**Description**: Search for models on the Hugging Face Hub with various filtering options.

**Parameters**:
- `query` (required): String - Search term (e.g., 'bert', 'gpt')
- `author` (optional): String - Filter by author/organization (e.g., 'huggingface', 'google')
- `tags` (optional): String - Filter by tags (e.g., 'text-classification', 'translation')
- `limit` (optional): Integer - Maximum number of results to return (default: 10)

**Example Usage**:
```json
call search-models {
  "query": "stable-diffusion",
  "author": "stabilityai",
  "tags": "text-to-image",
  "limit": 5
}
```

**Example Response**:
```json
{
  "success": true,
  "models": [
    {
      "id": "stabilityai/stable-diffusion-xl-base-1.0",
      "name": "Stable Diffusion XL 1.0",
      "description": "SDXL text-to-image model",
      "downloads": 1250000,
      "likes": 8500
    },
    {
      "id": "stabilityai/stable-diffusion-2-1",
      "name": "Stable Diffusion 2.1",
      "description": "Stable Diffusion version 2.1",
      "downloads": 1800000,
      "likes": 9800
    },
    {
      "id": "stabilityai/stable-diffusion-xl-refiner-1.0",
      "name": "SDXL Refiner 1.0",
      "description": "SDXL refiner model for enhanced details",
      "downloads": 980000,
      "likes": 6200
    }
  ]
}
```

#### `get-model-info`
**Description**: Get detailed information about a specific model on the Hugging Face Hub.

**Parameters**:
- `model_id` (required): String - The ID of the model (e.g., 'google/bert-base-uncased')

**Example Usage**:
```json
call get-model-info {
  "model_id": "meta-llama/Llama-3-8B-Instruct"
}
```

**Example Response**:
```json
{
  "success": true,
  "model": {
    "id": "meta-llama/Llama-3-8B-Instruct",
    "name": "Llama 3 8B Instruct",
    "description": "Meta's Llama 3 8B Instruct model for chat and instruction following",
    "downloads": 5200000,
    "likes": 18500,
    "tags": ["llm", "chat", "instruction-following"],
    "author": "Meta AI",
    "last_updated": "2025-03-15T14:30:00Z",
    "license": "llama-3",
    "model_size": "8B parameters",
    "architecture": "Transformer decoder",
    "context_length": 8192,
    "languages": ["English"],
    "training_data": ["Web data", "Books", "Code", "Mathematics"],
    "fine_tuning": "Instruction tuning with RLHF"
  }
}
```

### Dataset Tools

#### `search-datasets`
**Description**: Search for datasets on the Hugging Face Hub with various filtering options.

**Parameters**:
- `query` (optional): String - Search term
- `author` (optional): String - Filter by author/organization
- `tags` (optional): String - Filter by tags
- `limit` (optional): Integer - Maximum number of results to return (default: 10)

**Example Usage**:
```json
call search-datasets {
  "query": "squad",
  "tags": "question-answering",
  "limit": 3
}
```

**Example Response**:
```json
{
  "success": true,
  "datasets": [
    {
      "id": "squad",
      "name": "SQuAD",
      "description": "Stanford Question Answering Dataset",
      "downloads": 850000,
      "likes": 4200
    },
    {
      "id": "squad_v2",
      "name": "SQuAD v2",
      "description": "SQuAD 2.0 with unanswerable questions",
      "downloads": 720000,
      "likes": 3800
    },
    {
      "id": "deepmind/squad_es",
      "name": "SQuAD-es",
      "description": "Spanish translation of the SQuAD dataset",
      "downloads": 125000,
      "likes": 980
    }
  ]
}
```

#### `get-dataset-info`
**Description**: Get detailed information about a specific dataset on the Hugging Face Hub.

**Parameters**:
- `dataset_id` (required): String - The ID of the dataset (e.g., 'squad')

**Example Usage**:
```json
call get-dataset-info {
  "dataset_id": "squad"
}
```

**Example Response**:
```json
{
  "success": true,
  "dataset": {
    "id": "squad",
    "name": "SQuAD",
    "description": "Stanford Question Answering Dataset",
    "downloads": 850000,
    "likes": 4200,
    "tags": ["question-answering", "reading-comprehension", "english"],
    "author": "Stanford NLP Group",
    "last_updated": "2024-01-10T09:15:00Z",
    "license": "CC BY-SA 4.0",
    "size": "35MB",
    "num_examples": 100000,
    "languages": ["English"],
    "splits": ["train", "validation"],
    "features": ["context", "question", "answers"],
    "paper": "https://arxiv.org/abs/1606.05250"
  }
}
```

### Space Tools

#### `search-spaces`
**Description**: Search for Spaces on the Hugging Face Hub with various filtering options.

**Parameters**:
- `query` (optional): String - Search term
- `author` (optional): String - Filter by author/organization
- `tags` (optional): String - Filter by tags
- `sdk` (optional): String - Filter by SDK (e.g., 'streamlit', 'gradio', 'docker')
- `limit` (optional): Integer - Maximum number of results to return (default: 10)

**Example Usage**:
```json
call search-spaces {
  "query": "diffusion",
  "sdk": "gradio",
  "limit": 3
}
```

**Example Response**:
```json
{
  "success": true,
  "spaces": [
    {
      "id": "huggingface/diffusers-demo",
      "name": "Diffusers Demo",
      "description": "Demo of Stable Diffusion models",
      "sdk": "gradio",
      "views": 1250000,
      "likes": 8500
    },
    {
      "id": "prompthero/midjourney-v4-diffusion",
      "name": "Midjourney v4 Diffusion",
      "description": "Replica of Midjourney v4",
      "sdk": "gradio",
      "views": 980000,
      "likes": 7200
    },
    {
      "id": "multimodalart/stable-diffusion-inpainting",
      "name": "Stable Diffusion Inpainting",
      "description": "Inpainting with Stable Diffusion",
      "sdk": "gradio",
      "views": 750000,
      "likes": 5800
    }
  ]
}
```

#### `get-space-info`
**Description**: Get detailed information about a specific Space on the Hugging Face Hub.

**Parameters**:
- `space_id` (required): String - The ID of the Space (e.g., 'huggingface/diffusers-demo')

**Example Usage**:
```json
call get-space-info {
  "space_id": "huggingface/diffusers-demo"
}
```

**Example Response**:
```json
{
  "success": true,
  "space": {
    "id": "huggingface/diffusers-demo",
    "name": "Diffusers Demo",
    "description": "Interactive demo of Hugging Face Diffusers library with various models",
    "sdk": "gradio",
    "views": 1250000,
    "likes": 8500,
    "author": "Hugging Face",
    "last_updated": "2024-12-05T16:45:00Z",
    "tags": ["diffusion", "text-to-image", "image-generation"],
    "models_used": ["stabilityai/stable-diffusion-xl-base-1.0", "runwayml/stable-diffusion-v1-5"],
    "hardware": "A100",
    "runtime": "Python 3.10",
    "license": "Apache 2.0",
    "url": "https://huggingface.co/spaces/huggingface/diffusers-demo"
  }
}
```

### Paper Tools

#### `get-paper-info`
**Description**: Get information about a specific paper on Hugging Face, including its implementations.

**Parameters**:
- `arxiv_id` (required): String - The arXiv ID of the paper (e.g., '1810.04805')

**Example Usage**:
```json
call get-paper-info {
  "arxiv_id": "1810.04805"
}
```

**Example Response**:
```json
{
  "success": true,
  "paper": {
    "arxiv_id": "1810.04805",
    "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
    "authors": ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"],
    "abstract": "We introduce a new language representation model called BERT...",
    "published_date": "2018-10-11",
    "url": "https://arxiv.org/abs/1810.04805",
    "citations": 65000,
    "implementations": [
      {
        "id": "google/bert-base-uncased",
        "name": "BERT Base Uncased",
        "downloads": 12500000,
        "likes": 15800
      },
      {
        "id": "google/bert-large-uncased",
        "name": "BERT Large Uncased",
        "downloads": 8700000,
        "likes": 12300
      }
    ],
    "related_papers": [
      {
        "arxiv_id": "1906.08237",
        "title": "RoBERTa: A Robustly Optimized BERT Pretraining Approach"
      }
    ]
  }
}
```

#### `get-daily-papers`
**Description**: Get the list of daily papers curated by Hugging Face.

**Parameters**: None

**Example Usage**:
```json
call get-daily-papers {}
```

**Example Response**:
```json
{
  "success": true,
  "date": "2025-05-14",
  "papers": [
    {
      "arxiv_id": "2505.12345",
      "title": "Advanced Techniques for Multi-modal Learning in Large Language Models",
      "authors": ["Jane Smith", "John Doe"],
      "abstract": "This paper introduces novel techniques for multi-modal learning...",
      "url": "https://arxiv.org/abs/2505.12345",
      "category": "cs.CL"
    },
    {
      "arxiv_id": "2505.67890",
      "title": "Efficient Fine-tuning of Vision-Language Models for Domain-Specific Tasks",
      "authors": ["Alice Johnson", "Bob Brown"],
      "abstract": "We present a method for efficient fine-tuning of vision-language models...",
      "url": "https://arxiv.org/abs/2505.67890",
      "category": "cs.CV"
    },
    {
      "arxiv_id": "2505.54321",
      "title": "Scaling Laws for Autoregressive Generative Models",
      "authors": ["Charlie Davis", "Diana Evans"],
      "abstract": "This study investigates the scaling behavior of autoregressive generative models...",
      "url": "https://arxiv.org/abs/2505.54321",
      "category": "cs.LG"
    }
  ]
}
```

### Collection Tools

#### `search-collections`
**Description**: Search for collections on the Hugging Face Hub with various filtering options.

**Parameters**:
- `owner` (optional): String - Filter by owner
- `item` (optional): String - Filter by item (e.g., 'models/teknium/OpenHermes-2.5-Mistral-7B')
- `query` (optional): String - Search term for titles and descriptions
- `limit` (optional): Integer - Maximum number of results to return (default: 10)

**Example Usage**:
```json
call search-collections {
  "query": "llm",
  "limit": 3
}
```

**Example Response**:
```json
{
  "success": true,
  "collections": [
    {
      "id": "huggingface/top-open-llms",
      "name": "Top Open LLMs",
      "description": "A collection of the most popular open-source large language models",
      "items_count": 15,
      "likes": 3200
    },
    {
      "id": "TheBloke/quantized-llms",
      "name": "Quantized LLMs",
      "description": "Collection of quantized versions of popular LLMs for efficient inference",
      "items_count": 25,
      "likes": 2800
    },
    {
      "id": "argilla/llm-evaluation-datasets",
      "name": "LLM Evaluation Datasets",
      "description": "Datasets for benchmarking and evaluating LLM performance",
      "items_count": 10,
      "likes": 1500
    }
  ]
}
```

#### `get-collection-info`
**Description**: Get detailed information about a specific collection on the Hugging Face Hub.

**Parameters**:
- `namespace` (required): String - The namespace of the collection (user or organization)
- `collection_id` (required): String - The ID part of the collection

**Example Usage**:
```json
call get-collection-info {
  "namespace": "huggingface",
  "collection_id": "top-open-llms"
}
```

**Example Response**:
```json
{
  "success": true,
  "collection": {
    "id": "huggingface/top-open-llms",
    "name": "Top Open LLMs",
    "description": "A curated collection of the most popular and powerful open-source large language models",
    "created_at": "2024-08-15T10:20:30Z",
    "updated_at": "2025-04-28T14:25:45Z",
    "likes": 3200,
    "author": "Hugging Face",
    "items": [
      {
        "type": "model",
        "id": "meta-llama/Llama-3-8B-Instruct",
        "name": "Llama 3 8B Instruct"
      },
      {
        "type": "model",
        "id": "mistralai/Mistral-7B-Instruct-v0.2",
        "name": "Mistral 7B Instruct v0.2"
      },
      {
        "type": "model",
        "id": "openchat/openchat-3.5-0106",
        "name": "OpenChat 3.5"
      }
    ],
    "tags": ["llm", "open-source", "instruction-following", "chat"]
  }
}
```

## Available Tools

The Hugging Face Hub Agent provides access to the following tool categories:

### Model Tools
- `search-models`: Search models with filters for query, author, tags, and limit
- `get-model-info`: Get detailed information about a specific model

### Dataset Tools
- `search-datasets`: Search datasets with filters
- `get-dataset-info`: Get detailed information about a specific dataset

### Space Tools
- `search-spaces`: Search Spaces with filters including SDK type
- `get-space-info`: Get detailed information about a specific Space

### Paper Tools
- `get-paper-info`: Get information about a paper and its implementations
- `get-daily-papers`: Get the list of curated daily papers

### Collection Tools
- `search-collections`: Search collections with various filters
- `get-collection-info`: Get detailed information about a specific collection

## Example

```python
from hugging_face_hub.agent import HuggingFaceHubAgent

agent = HuggingFaceHubAgent()

# List available tools
agent.process_message("!list")

# Search for models
agent.process_message('!shorthand search-models query="stable-diffusion" limit=5')

# Get model info
agent.process_message('!shorthand get-model-info model_id="meta-llama/Llama-3-8B-Instruct"')
```

For more examples, see the `examples` directory, particularly `huggingface_client.py`.

## License

[MIT License](LICENSE)