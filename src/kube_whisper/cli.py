from typing import Literal
from kube_whisper.function_registry import FunctionRegistry

@FunctionRegistry.register(
    description="Get weather data",
    response_template="The temperature in {location} is {temp} {unit}"
)
def get_current_weather(location: str, unit: Literal["celsius", "fahrenheit"]):
    pass
