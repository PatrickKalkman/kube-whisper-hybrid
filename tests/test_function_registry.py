import json
import unittest
from kubewhisper.registry.function_registry import FunctionRegistry


class TestFunctionRegistry(unittest.TestCase):
    def test_register_function(self):
        FunctionRegistry.functions = []  # Reset the registry

        @FunctionRegistry.register(description="Test function", response_template="Test response")
        def test_func(param1: str):
            pass

        self.assertEqual(len(FunctionRegistry.functions), 1)

    def test_generate_json_schema(self):
        FunctionRegistry.functions = []  # Reset the registry

        @FunctionRegistry.register(description="Test function", response_template="Test response")
        def test_func(param1: str):
            pass

        json_schema = FunctionRegistry.generate_json_schema()
        self.assertTrue(json_schema)

        # Optionally, parse the JSON and verify its contents
        schema = json.loads(json_schema)
        self.assertEqual(len(schema), 1)
        self.assertEqual(schema[0]["name"], "test_func")


if __name__ == "__main__":
    unittest.main()
