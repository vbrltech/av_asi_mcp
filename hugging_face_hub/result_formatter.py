"""
Result Formatter - Format API responses for chat

This module contains the ResultFormatter class that formats API responses
into readable chat messages, handles different result types, and creates
readable output.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ResultFormatter:
    """Formatter for API responses and other outputs."""
    
    def __init__(self, max_json_depth: int = 3, indent_size: int = 2):
        """
        Initialize the result formatter.
        
        Args:
            max_json_depth: Maximum depth for JSON formatting
            indent_size: Number of spaces for indentation
        """
        self.max_json_depth = max_json_depth
        self.indent_size = indent_size
    
    def format_connect_result(self, result: Dict[str, Any]) -> str:
        """
        Format a connection result.
        
        Args:
            result: The connection result
            
        Returns:
            Formatted message
        """
        if result.get("success", False):
            message = f"✅ {result.get('message', 'Connected successfully')}"
            if "tool_count" in result:
                message += f"\n\nFound {result['tool_count']} available tools. Use `list` to see them."
            return message
        else:
            return f"❌ {result.get('message', 'Connection failed')}"
    
    def format_disconnect_result(self, result: Dict[str, Any]) -> str:
        """
        Format a disconnection result.
        
        Args:
            result: The disconnection result
            
        Returns:
            Formatted message
        """
        if result.get("success", False):
            return f"✅ {result.get('message', 'Disconnected successfully')}"
        else:
            return f"❌ {result.get('message', 'Disconnection failed')}"
    
    def format_tool_list(self, tools: List[Any]) -> str:
        """
        Format a list of tools.
        
        Args:
            tools: The list of tools
            
        Returns:
            Formatted message
        """
        if not tools:
            return "No tools available. Make sure you're connected to the Hugging Face Hub API server."
        
        result = f"📋 Available Tools ({len(tools)}):\n\n"
        
        for tool in tools:
            # Handle both dictionary-like objects and Tool objects
            if hasattr(tool, 'name'):
                name = tool.name
            elif isinstance(tool, dict) and "name" in tool:
                name = tool["name"]
            else:
                name = "Unknown"
                
            if hasattr(tool, 'description'):
                description = tool.description
            elif isinstance(tool, dict) and "description" in tool:
                description = tool["description"]
            else:
                description = "No description available"
            
            # Add tool name and description
            result += f"**{name}**\n{description}\n\n"
            
            # Add schema information if available
            schema = None
            if hasattr(tool, 'schema'):
                schema = tool.schema
            elif hasattr(tool, 'parameters'):
                schema = tool.parameters
            elif hasattr(tool, 'parameter_schema'):
                schema = tool.parameter_schema
            elif hasattr(tool, 'inputSchema'):
                schema = tool.inputSchema
            elif isinstance(tool, dict) and "schema" in tool:
                schema = tool["schema"]
            
            if schema and hasattr(schema, 'get'):
                properties = schema.get("properties", {})
                required = schema.get("required", [])
                
                if properties:
                    result += "Arguments:\n"
                    for prop_name, prop_info in properties.items():
                        if hasattr(prop_info, 'get'):
                            prop_type = prop_info.get("type", "any")
                            prop_desc = prop_info.get("description", "")
                        elif isinstance(prop_info, dict):
                            prop_type = prop_info.get("type", "any")
                            prop_desc = prop_info.get("description", "")
                        else:
                            prop_type = "any"
                            prop_desc = ""
                            
                        is_required = prop_name in required
                        
                        req_marker = "*" if is_required else ""
                        result += f"- `{prop_name}`{req_marker}: {prop_type}"
                        if prop_desc:
                            result += f" - {prop_desc}"
                        result += "\n"
                    
                    result += "\n"
        
        result += "Use `call [tool_name] {\"arg\": \"value\"}` to call a tool.\n"
        result += "Or use the shorthand syntax: `shorthand [tool_name] arg=\"value\"`"
        
        return result
    
    def format_tool_call_result(self, result: Dict[str, Any]) -> str:
        """
        Format a tool call result.
        
        Args:
            result: The tool call result
            
        Returns:
            Formatted message
        """
        if not result.get("success", False):
            return f"❌ {result.get('message', 'Tool call failed')}"
        
        tool_result = result.get("result")
        
        # Format the result based on its type
        if isinstance(tool_result, dict) or isinstance(tool_result, list):
            formatted_result = self.format_json(tool_result)
        elif tool_result is None:
            formatted_result = "No result returned"
        else:
            formatted_result = str(tool_result)
        
        return f"✅ Tool call successful:\n\n```\n{formatted_result}\n```"
    
    def format_status(self, status: Dict[str, Any]) -> str:
        """
        Format a connection status.
        
        Args:
            status: The connection status
            
        Returns:
            Formatted message
        """
        if not status.get("connected", False):
            return f"📡 Status: {status.get('message', 'Not connected')}"
        
        message = f"📡 Status: Connected to {status.get('url', 'unknown')}"
        
        if "tool_count" in status:
            message += f"\nAvailable tools: {status['tool_count']}"
        
        if status.get("has_token", False):
            message += "\nAuthentication: Using token"
        else:
            message += "\nAuthentication: None"
        
        return message
    
    def format_error(self, message: str) -> str:
        """
        Format an error message.
        
        Args:
            message: The error message
            
        Returns:
            Formatted message
        """
        return f"❌ Error: {message}"
    
    def format_parameter_validation_error(self, tool_name: str, message: str, schema: Optional[Dict[str, Any]] = None) -> str:
        """
        Format a parameter validation error message with helpful information.
        
        Args:
            tool_name: The name of the tool
            message: The error message
            schema: Optional schema information for the tool
            
        Returns:
            Formatted message
        """
        result = f"❌ Parameter validation error for tool '{tool_name}':\n{message}\n\n"
        
        # Add schema information if available
        if schema and isinstance(schema, dict):
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            
            if properties:
                result += "Required parameters:\n"
                for prop_name in required:
                    prop_info = properties.get(prop_name, {})
                    prop_type = prop_info.get("type", "any")
                    prop_desc = prop_info.get("description", "")
                    
                    result += f"- `{prop_name}`: {prop_type}"
                    if prop_desc:
                        result += f" - {prop_desc}"
                    result += "\n"
                
                # Add example usage
                result += "\nExample usage:\n"
                example = {}
                for prop_name in required:
                    prop_info = properties.get(prop_name, {})
                    prop_type = prop_info.get("type", "any")
                    
                    # Generate example value based on type
                    if prop_type == "string":
                        example[prop_name] = "example_string"
                    elif prop_type == "number" or prop_type == "integer":
                        example[prop_name] = 42
                    elif prop_type == "boolean":
                        example[prop_name] = True
                    elif prop_type == "array":
                        example[prop_name] = []
                    elif prop_type == "object":
                        example[prop_name] = {}
                    else:
                        example[prop_name] = "value"
                
                result += f"```\ncall {tool_name} {json.dumps(example, indent=2)}\n```"
        
        return result
    
    def format_json(self, data: Union[Dict, List, Any], depth: int = 0) -> str:
        """
        Format JSON data with proper indentation and truncation.
        
        Args:
            data: The data to format
            depth: Current depth level
            
        Returns:
            Formatted JSON string
        """
        if depth >= self.max_json_depth:
            if isinstance(data, dict) and data:
                return "{...}"
            elif isinstance(data, list) and data:
                return "[...]"
        
        if isinstance(data, dict):
            if not data:
                return "{}"
            
            indent = " " * self.indent_size * depth
            next_indent = " " * self.indent_size * (depth + 1)
            
            parts = []
            for key, value in data.items():
                formatted_value = self.format_json(value, depth + 1)
                parts.append(f"{next_indent}\"{key}\": {formatted_value}")
            
            return "{\n" + ",\n".join(parts) + f"\n{indent}}}"
        
        elif isinstance(data, list):
            if not data:
                return "[]"
            
            indent = " " * self.indent_size * depth
            next_indent = " " * self.indent_size * (depth + 1)
            
            parts = []
            for item in data:
                formatted_item = self.format_json(item, depth + 1)
                parts.append(f"{next_indent}{formatted_item}")
            
            return "[\n" + ",\n".join(parts) + f"\n{indent}]"
        
        elif isinstance(data, str):
            return f"\"{data}\""
        
        elif data is None:
            return "null"
        
        else:
            return str(data)
    
    def format_unknown_command(self, command: str) -> str:
        """
        Format an unknown command message.
        
        Args:
            command: The unknown command
            
        Returns:
            Formatted message
        """
        return (
            f"❓ Unknown command: `{command}`\n\n"
            "Use `help` to see available commands."
        )
    
    def format_not_connected_error(self) -> str:
        """
        Format a not connected error message.
        
        Returns:
            Formatted message
        """
        return (
            "❌ Not connected to the Hugging Face Hub API server.\n\n"
            "Use `connect` to connect to the API server."
        )
    
    def format_schema_result(self, tool_name: str, schema: Dict[str, Any]) -> str:
        """
        Format a schema result.
        
        Args:
            tool_name: The name of the tool
            schema: The schema to format
            
        Returns:
            Formatted message
        """
        result = f"📝 Schema for tool '{tool_name}':\n\n"
        
        # Check if schema is valid
        if not schema:
            return f"❌ No schema available for tool '{tool_name}'"
        
        if not isinstance(schema, dict):
            return f"❌ Invalid schema format for tool '{tool_name}': {type(schema).__name__}"
        
        # Add schema information
        if "title" in schema:
            result += f"**Title**: {schema['title']}\n\n"
        
        if "description" in schema:
            result += f"**Description**: {schema['description']}\n\n"
        
        # Add properties
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        if not properties:
            result += "**No parameters defined in schema**\n\n"
        else:
            # Count required and optional parameters
            req_count = sum(1 for p in properties if p in required)
            opt_count = len(properties) - req_count
            
            result += f"**Parameters** ({req_count} required, {opt_count} optional):\n\n"
            
            # Sort properties to show required parameters first
            sorted_props = sorted(properties.items(),
                                 key=lambda x: (0 if x[0] in required else 1, x[0]))
            
            for prop_name, prop_info in sorted_props:
                if not isinstance(prop_info, dict):
                    continue
                
                is_required = prop_name in required
                req_marker = " (required)" if is_required else " (optional)"
                
                prop_type = prop_info.get("type", "any")
                prop_desc = prop_info.get("description", "")
                
                # Format the parameter name and type with appropriate styling
                result += f"- **`{prop_name}`**{req_marker}: `{prop_type}`\n"
                
                # Add description with proper indentation
                if prop_desc:
                    # Format description with proper indentation
                    result += f"  {prop_desc}\n"
                
                # Add constraints section if any constraints exist
                constraints = []
                
                # Add enum values if available
                if "enum" in prop_info:
                    enum_values = prop_info["enum"]
                    if len(enum_values) <= 5:  # Show all values if 5 or fewer
                        constraints.append(f"Allowed values: {', '.join([f'`{v}`' for v in enum_values])}")
                    else:  # Show count if more than 5
                        constraints.append(f"Allowed values: {len(enum_values)} options")
                
                # Add default value if available
                if "default" in prop_info:
                    default_value = prop_info["default"]
                    if default_value is None:
                        constraints.append("Default: `null`")
                    elif isinstance(default_value, str):
                        constraints.append(f"Default: `\"{default_value}\"`")
                    else:
                        constraints.append(f"Default: `{default_value}`")
                
                # Add min/max values for numbers
                if prop_type in ["number", "integer"]:
                    if "minimum" in prop_info:
                        constraints.append(f"Minimum: `{prop_info['minimum']}`")
                    if "maximum" in prop_info:
                        constraints.append(f"Maximum: `{prop_info['maximum']}`")
                
                # Add min/max length for strings
                if prop_type == "string":
                    if "minLength" in prop_info:
                        constraints.append(f"Minimum length: `{prop_info['minLength']}`")
                    if "maxLength" in prop_info:
                        constraints.append(f"Maximum length: `{prop_info['maxLength']}`")
                    if "format" in prop_info:
                        constraints.append(f"Format: `{prop_info['format']}`")
                
                # Add pattern for strings
                if prop_type == "string" and "pattern" in prop_info:
                    constraints.append(f"Pattern: `{prop_info['pattern']}`")
                
                # Add constraints for arrays
                if prop_type == "array":
                    if "minItems" in prop_info:
                        constraints.append(f"Minimum items: `{prop_info['minItems']}`")
                    if "maxItems" in prop_info:
                        constraints.append(f"Maximum items: `{prop_info['maxItems']}`")
                    if "uniqueItems" in prop_info and prop_info["uniqueItems"]:
                        constraints.append("Items must be unique")
                
                # Add all constraints with proper indentation
                if constraints:
                    result += "  " + "\n  ".join(constraints) + "\n"
                
                result += "\n"
        
        # Add example usage
        result += "**Example Usage**:\n\n"
        example = {}
        
        # Add required parameters to example
        for prop_name in required:
            if prop_name not in properties:
                continue
                
            prop_info = properties.get(prop_name, {})
            prop_type = prop_info.get("type", "any")
            
            # Generate example value based on type
            if "example" in prop_info:
                example[prop_name] = prop_info["example"]
            elif "default" in prop_info:
                example[prop_name] = prop_info["default"]
            elif "enum" in prop_info and prop_info["enum"]:
                example[prop_name] = prop_info["enum"][0]
            elif prop_type == "string":
                if "format" in prop_info:
                    if prop_info["format"] == "date":
                        example[prop_name] = "2023-01-01"
                    elif prop_info["format"] == "date-time":
                        example[prop_name] = "2023-01-01T12:00:00Z"
                    elif prop_info["format"] == "email":
                        example[prop_name] = "user@example.com"
                    elif prop_info["format"] == "uri":
                        example[prop_name] = "https://example.com"
                    else:
                        example[prop_name] = f"example_{prop_info['format']}"
                else:
                    example[prop_name] = f"example_{prop_name}"
            elif prop_type == "number":
                example[prop_name] = 42.0
            elif prop_type == "integer":
                example[prop_name] = 42
            elif prop_type == "boolean":
                example[prop_name] = True
            elif prop_type == "array":
                if "items" in prop_info and "type" in prop_info["items"]:
                    items_type = prop_info["items"]["type"]
                    if items_type == "string":
                        example[prop_name] = ["example"]
                    elif items_type == "number":
                        example[prop_name] = [42.0]
                    elif items_type == "integer":
                        example[prop_name] = [42]
                    elif items_type == "boolean":
                        example[prop_name] = [True]
                    else:
                        example[prop_name] = []
                else:
                    example[prop_name] = []
            elif prop_type == "object":
                example[prop_name] = {}
            else:
                example[prop_name] = None
        
        # Add some optional parameters with defaults as examples
        optional_count = 0
        for prop_name, prop_info in properties.items():
            if prop_name not in required and optional_count < 3:
                if "default" in prop_info:
                    example[prop_name] = prop_info["default"]
                    optional_count += 1
        
        # Format the example with proper indentation
        try:
            example_json = json.dumps(example, indent=2)
        except Exception:
            example_json = "{}"
        
        # Show both natural language and structured command examples
        result += f"```\n# Natural language command:\nschema {tool_name}\n\n"
        result += f"# Structured command:\n!schema {tool_name}\n\n"
        result += f"# Tool call example:\ncall {tool_name} {example_json}\n```\n\n"
        
        # Add raw schema with a collapsible section
        result += "**Raw Schema**:\n\n"
        try:
            # Limit the raw schema to a reasonable size
            schema_json = json.dumps(schema, indent=2)
            if len(schema_json) > 2000:
                schema_json = schema_json[:2000] + "\n... (truncated)"
            result += f"```json\n{schema_json}\n```"
        except Exception as e:
            result += f"```\nError formatting schema: {e}\n```"
        
        return result