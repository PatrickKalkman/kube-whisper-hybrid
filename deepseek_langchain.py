import os
from langchain_openai.chat_models.base import BaseChatOpenAI
import json

tools = [
    {
        "type": "function",
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city name"},
                "unit": {
                    "type": "string",
                    "description": "Temperature unit",
                    "enum": ["celsius", "fahrenheit"],
                },
            },
            "required": ["location", "unit"],
        },
    },
    {
        "type": "function",
        "name": "get_air_quality",
        "description": "Get air quality information for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city name"},
                "index": {
                    "type": "string",
                    "description": "Type of air quality index",
                    "enum": ["aqi", "pm25"],
                },
            },
            "required": ["location", "index"],
        },
    },
    {
        "type": "function",
        "name": "get_number_of_namespaces",
        "description": "Returns the number of namespaces in a Kubernetes cluster.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]


def validate_response(response_json, tools):
    if "name" not in response_json:
        raise ValueError("Missing name field")

    tool = next((t for t in tools if t["name"] == response_json["name"]), None)
    if not tool:
        raise ValueError(f"Invalid function name: {response_json['name']}")

    params = response_json.get("parameters", {})
    properties = tool["parameters"]["properties"]
    required = tool["parameters"]["required"]

    for param in required:
        if param not in params:
            raise ValueError(f"Missing required parameter: {param}")
        if "enum" in properties[param]:
            if params[param] not in properties[param]["enum"]:
                raise ValueError(f"Invalid {param} value: {params[param]}")

    return True


llm = BaseChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.environ["DEEPSEEK_API_KEY"],
    openai_api_base="https://api.deepseek.com",
    max_tokens=1024,
)

question = "How are you doing?"

prompt = f"""Available functions for data queries:
{json.dumps(tools, indent=2)}

Instructions:
1. If the question asks for data that can be retrieved using one of the function, return a function call JSON without backticks or formatting.
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

try:
    response = llm.invoke(prompt)
    content = response.content.strip()
    if content.startswith("{"):
        try:
            parsed_response = json.loads(content)
            validate_response(parsed_response, tools)
            print(json.dumps(parsed_response, indent=2))
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error: {e}")
    else:
        print(content)
except json.JSONDecodeError:
    print("Error: Invalid JSON response")
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
