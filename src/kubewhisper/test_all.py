import unittest
from kubewhisper.registry.function_registry import FunctionRegistry
from kubewhisper.llm.deepseek import DeepSeekLLM


class TestDeepSeekLLM(unittest.TestCase):
    def setUp(self):
        """Set up the DeepSeekLLM instance before each test."""
        self.deepseek_llm = DeepSeekLLM()

    def test_registered_functions(self):
        """Test that the LLM returns the correct function for each registered function description."""
        # Get all registered functions
        functions = FunctionRegistry.functions

        for func in functions:
            with self.subTest(function=func.__name__):
                # Use the function's description as the question
                question = func.metadata['description']
                # Send the question to the LLM
                response = self.deepseek_llm.ask_question(question)
                # Verify that the correct function is identified
                if 'name' in response:
                    self.assertEqual(response['name'], func.__name__)
                else:
                    self.fail(f"LLM did not return a function for: {question}")


if __name__ == '__main__':
    unittest.main()
