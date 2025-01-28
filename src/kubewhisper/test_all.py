import unittest
import logging
from kubewhisper.registry.function_registry import FunctionRegistry
from kubewhisper.llm.deepseek import DeepSeekLLM
from kubewhisper.k8s import k8s_tools  # noqa: F401

# Configure logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TestDeepSeekLLM(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """Set up the DeepSeekLLM instance before each test."""
        logging.info("Setting up DeepSeekLLM instance.")
        self.deepseek_llm = DeepSeekLLM()

    def _generate_test_parameters(self, func) -> dict:
        """Generate test parameters for a function based on its metadata."""
        param_values = {}
        if hasattr(func, "metadata") and func.metadata.get("parameters"):
            for param_name, param_info in func.metadata["parameters"].get("properties", {}).items():
                if param_info.get("type") == "string":
                    param_values[param_name] = f"test_{param_name}"
                elif param_info.get("type") == "integer":
                    param_values[param_name] = 42
        return param_values

    def _verify_response(self, response: dict, expected_func_name: str, param_values: dict):
        """Verify the LLM response matches expected function and parameters."""
        if "name" not in response:
            self.fail(f"LLM did not return a function for: {expected_func_name}")
        
        self.assertEqual(response["name"], expected_func_name)
        
        if param_values and "parameters" in response:
            for param_name, param_value in param_values.items():
                self.assertEqual(
                    response["parameters"].get(param_name), 
                    param_value,
                    f"Parameter mismatch for {param_name}"
                )

    async def test_registered_functions(self):
        """Test that the LLM returns the correct function for each registered function description."""
        functions = FunctionRegistry.functions
        logging.info(f"Testing {len(functions)} registered functions.")
        
        for func in functions:
            with self.subTest(function=func.__name__):
                # Get function description and generate test parameters
                question = func.metadata["description"]
                param_values = self._generate_test_parameters(func)
                
                logging.info(f"Testing {func.__name__}")
                logging.info(f"Question: {question}")
                logging.info(f"Parameters: {param_values}")
                
                # Get LLM response
                response = await self.deepseek_llm.ask_question(question, **param_values)
                logging.info(f"Response: {response}")
                
                # Verify response
                self._verify_response(response, func.__name__, param_values)


if __name__ == "__main__":
    unittest.main()
