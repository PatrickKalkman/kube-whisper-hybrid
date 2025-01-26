"""
Function registry implementation.
"""

class FunctionRegistry:
    def __init__(self):
        self._functions = {}

    def register(self, name: str):
        """Decorator to register a function"""
        def decorator(func):
            self._functions[name] = func
            return func
        return decorator

    def get_function(self, name: str):
        """Get a registered function by name"""
        return self._functions.get(name)

    def list_functions(self):
        """List all registered functions"""
        return list(self._functions.keys())
