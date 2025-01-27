import unittest
import logging
from kubewhisper.registry.function_registry import FunctionRegistry
from kubewhisper.llm.deepseek import DeepSeekLLM
from kubewhisper.k8s import k8s_tools

# Configure logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TestDeepSeekLLM(unittest.TestCase):
    def setUp(self):
        """Set up the DeepSeekLLM instance before each test."""
        logging.info("Setting up DeepSeekLLM instance.")
        self.deepseek_llm = DeepSeekLLM()

    def test_registered_functions(self):
        """Test that the LLM returns the correct function for each registered function description."""
        # Get all registered functions
        functions = FunctionRegistry.functions
        logging.info(f"Testing {len(functions)} registered functions.")
        for func in functions:
            with self.subTest(function=func.__name__):
                # Use the function's description as the question
                question = func.metadata["description"]
                logging.info(f"Testing function: {func.__name__} with question: '{question}'")

                # Generate random parameter values if the function has parameters
                param_values = {}
                if hasattr(func, 'metadata') and func.metadata.get('parameters'):
                    for param_name, param_info in func.metadata['parameters'].get('properties', {}).items():
                        if param_info.get('type') == 'string':
                            param_values[param_name] = f"test_{param_name}"
                        elif param_info.get('type') == 'integer':
                            param_values[param_name] = 42
                
                # Send the question to the LLM with parameters
                logging.info(f"Testing function: {func.__name__} with question: '{question}' and parameters: {param_values}")
                response = self.deepseek_llm.ask_question(question, **param_values)
                logging.info(f"Received response: {response}")
                
                # Verify parameters in response if they were provided
                if param_values and "parameters" in response:
                    for param_name, param_value in param_values.items():
                        self.assertEqual(response["parameters"].get(param_name), param_value)
                # Verify that the correct function is identified
                if "name" in response:
                    self.assertEqual(response["name"], func.__name__)
                else:
                    self.fail(f"LLM did not return a function for: {question}")


if __name__ == "__main__":
    unittest.main()
