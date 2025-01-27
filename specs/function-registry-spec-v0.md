# Transcript Analytics v0 Specification

## High-Level Objective

- Create a function registry for registering functions and generate the json schema from the registered functions.

## Mid-Level Objective

- Build a function registry for registering functions that can be called in response to a LLM 
- It should be able to support function registration like shown in example 1
- It should have a function to generate a json schema string from all the registered function as shown in example 2
- Add a test to register a function and assert that the number of functions is 1
- Add a test that registers a function and validates that the json is generated successfully

## Implementation Notes
- No need to import any external libraries see pyproject.toml for dependencies.
- Comment every function.
- Use type hints 
- When code block is given in low-level tasks, use it without making changes (Task 4).
- Carefully review each low-level task for exact code changes.

## Context

### Beginning context
- `src/kube_whisper/cli.py`
- `pyproject.toml` (readonly)

### Ending context
- `src/kube_whisper/cli.py`
- `src/kube_whisper/function_registry.py
- `tests/test_function_registry.py`
- `pyproject.toml` (readonly)


## Low-Level Examples
> Ordered from start to finish

1. Use this example
@FunctionRegistry.register(
    description="Get weather data",
    response_template="The temperature in {location} is {temp} {unit}"
)
def get_current_weather(location: str, unit: Literal["celsius", "fahrenheit"]):
    pass

2. We generate the following json from the example in 1 if only one function, if more functions are registered we generate multiple objects in an array. 
[{
    "type": "function",
    "name": "get_current_weather",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["location", "unit"]
    }
}]