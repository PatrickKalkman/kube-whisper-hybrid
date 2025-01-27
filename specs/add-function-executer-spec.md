# Transcript Analytics v0 Specification

## High-Level Objective

- Create a class FunctionExecutor for executing the identified function in the response from the LLM with the correct parameters

## Mid-Level Objective
- Use the response from the ask_question function in the deepseek.py file as an input to the FunctionExecuter
- Call the identified function with the identified parameters
- Log the calling of the function.
- Generate an error if the function does not exist

## Implementation Notes
- No need to import any external libraries see pyproject.toml for dependencies.
- Comment every function.
- Use type hints 
- When code block is given in low-level tasks, use it without making changes (Task 4).
- Carefully review each low-level task for exact code changes.

## Context

### Beginning context
- `src/kube_whisper/k8s/k8s_tools.py`
- `src/kube_whisper/registry/function_registry.py`
- `src/kube_whisper/llm/deepseek.py`
- `pyproject.toml` (readonly)

### Ending context
- `src/kube_whisper/k8s/k8s_tools.py`
- `src/kube_whisper/registry/function_registry.py`
- `src/kube_whisper/llm/deepseek.py`
- `src/kube_whisper/function_executer.py`
- `pyproject.toml` (readonly)

## Low-Level Examples
> Ordered from start to finish
