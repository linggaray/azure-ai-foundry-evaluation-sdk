import os
import pytest
from dotenv import load_dotenv
from evaluators.coherence_evaluator import CoherenceEvaluatorWrapper
from azure.ai.evaluation import AzureOpenAIModelConfiguration

@pytest.fixture(scope="session")
def model_config():
    """Fixture to provide Azure OpenAI model configuration."""
    load_dotenv()
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not all([azure_endpoint, api_key, azure_deployment, api_version]):
        pytest.skip("Azure environment variables not set")

    return AzureOpenAIModelConfiguration(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        azure_deployment=azure_deployment,
        api_version=api_version,
    )

def test_coherence_evaluator_initialization(model_config):
    """Test that CoherenceEvaluatorWrapper can be initialized."""
    evaluator = CoherenceEvaluatorWrapper(model_config=model_config, threshold=3)
    assert evaluator is not None

def test_coherence_evaluator_evaluate(model_config):
    """Test the evaluate method of CoherenceEvaluatorWrapper."""
    evaluator = CoherenceEvaluatorWrapper(model_config=model_config, threshold=3)
    query = "What is the capital of France?"
    response = "The capital of France is Paris."
    result = evaluator.evaluate(query=query, response=response)
    print(f"Coherence evaluation result: {result}")
    assert isinstance(result, dict)
    assert 'coherence' in result
    assert 'coherence_result' in result