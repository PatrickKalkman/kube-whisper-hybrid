"""
DeepSeek LLM integration.
"""

import os
import json
from typing import Any, Dict, List
from langchain_openai.chat_models.base import BaseChatOpenAI
from kubewhisper.registry.function_registry import FunctionRegistry


class DeepSeekLLM:
    """Class to interact with the DeepSeek LLM."""

    def __init__(self):
        """Initialize the DeepSeek LLM with necessary configurations."""
        self.llm = BaseChatOpenAI(
            model="deepseek/deepseek-chat",
            openai_api_key=os.environ["DEEPSEEK_API_KEY"],
            openai_api_base="https://openrouter.ai/api/v1",
            max_tokens=1024,
        )

    def get_tools(self) -> List[Dict[str, Any]]:
        """Retrieve registered functions and generate the tools list."""
        tools_json = FunctionRegistry.generate_json_schema()
        tools = json.loads(tools_json)
        return tools

    def generate_prompt(self, question: str, tools: List[Dict[str, Any]]) -> str:
        """Generate the prompt to send to the LLM."""
        tools_formatted = json.dumps(tools, indent=2)
        prompt = f"""Available functions for data queries:
{tools_formatted}

Instructions:
1. If the question asks for data that can be retrieved using one of the functions,
return a function call JSON without backticks or formatting.
2. If it's a general question, conversation, or opinion, return a normal text response.
3. If unsure, attempt to provide a helpful text response.

Example function calls:
Weather query: "What's the temperature in Paris?"
{{
   "type": "function",
   "name": "get_current_weather",
   "parameters": {{
       "location": "Paris",
       "unit": "celsius"
   }}
}}

Air quality query: "How's the air in Beijing?"
{{
   "type": "function",
   "name": "get_air_quality",
   "parameters": {{
       "location": "Beijing",
       "index": "aqi"
   }}
}}

Example text responses:
- "What's the history of Amsterdam?" -> Historical information about Amsterdam...
- "Should I visit Amsterdam?" -> Travel advice about Amsterdam...

Question: {question}"""
        return prompt

    def validate_response(self, response_json: Dict[str, Any], tools: List[Dict[str, Any]]) -> bool:
        """Validate the LLM's JSON response against the tools schema."""
        if "name" not in response_json:
            raise ValueError("Missing 'name' field in response.")

        tool = next((t for t in tools if t["name"] == response_json["name"]), None)
        if not tool:
            raise ValueError(f"Invalid function name: {response_json['name']}")

        params = response_json.get("parameters", {})
        properties = tool["parameters"]["properties"]
        required = tool["parameters"].get("required", [])

        for param in required:
            if param not in params:
                raise ValueError(f"Missing required parameter: {param}")
            property_schema = properties.get(param, {})
            if "enum" in property_schema:
                if params[param] not in property_schema["enum"]:
                    raise ValueError(f"Invalid value for {param}: {params[param]}")

        return True

    async def execute_function_call(self, parsed_response: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a function based on the parsed LLM response."""
        from kubewhisper.registry.function_executor import FunctionExecutor

        func_name = parsed_response.get("name")
        func = next((f for f in FunctionRegistry.functions if f.__name__ == func_name), None)

        if not func:
            return {"error": f"Function {func_name} not found"}

        try:
            result = await FunctionExecutor.execute_function(func, **parsed_response.get("parameters", {}))
            return result
        except Exception as e:
            return {"error": f"Function execution error: {str(e)}"}

    async def ask_question(self, question: str, **kwargs) -> Dict[str, Any]:
        """Send the question to the LLM and process the response."""
        tools = self.get_tools()
        prompt = self.generate_prompt(question, tools)

        if kwargs:
            params_json = json.dumps(kwargs, indent=2)
            prompt += f"\n\nParameters for the function call:\n{params_json}"

        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content.strip()

            if content.startswith("{"):
                try:
                    parsed_response = json.loads(content)
                    self.validate_response(parsed_response, tools)
                    return parsed_response
                except (json.JSONDecodeError, ValueError) as e:
                    return {"error": f"Validation error: {str(e)}"}
            else:
                return {"response": content}

        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
