import os
import pytest
from dotenv import load_dotenv
from evaluators.qa_evaluator import QAEvaluatorWrapper
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

def test_qa_evaluator_initialization(model_config):
    """Test that QAEvaluatorWrapper can be initialized."""
    evaluator = QAEvaluatorWrapper(model_config=model_config, threshold=3)
    assert evaluator is not None

def test_qa_evaluator_evaluate(model_config):
    """Test the evaluate method of QAEvaluatorWrapper."""
    evaluator = QAEvaluatorWrapper(model_config=model_config, threshold=3)
    query = "What is the capital of France?"
    context = "France is a country in Europe."
    response = "The capital of France is Paris."
    ground_truth = "Paris"
    result = evaluator.evaluate(query=query, context=context, response=response, ground_truth=ground_truth)
    print(f"QA evaluation result: {result}")
    assert isinstance(result, dict)
    assert 'f1_score' in result
    assert 'similarity' in result