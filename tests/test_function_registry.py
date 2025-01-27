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


    def test_generate_json_schema_multiple_functions(self):
        # Reset the registry
        FunctionRegistry.functions = []

        # Register the first test function
        @FunctionRegistry.register(
            description="Test function one",
            response_template="Response one"
        )
        def test_func_one(param1: str):
            pass

        # Register the second test function
        @FunctionRegistry.register(
            description="Test function two",
            response_template="Response two"
        )
        def test_func_two(param2: int):
            pass

        # Generate the JSON schema
        json_schema = FunctionRegistry.generate_json_schema()
        self.assertTrue(json_schema)

        # Parse the JSON and verify its contents
        schema = json.loads(json_schema)
        self.assertIsInstance(schema, list)
        self.assertEqual(len(schema), 2)
        self.assertEqual(schema[0]["name"], "test_func_one")
        self.assertEqual(schema[1]["name"], "test_func_two")


if __name__ == "__main__":
    unittest.main()
