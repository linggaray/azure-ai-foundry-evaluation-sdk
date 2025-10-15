import json
import os
from evaluators.coherence_evaluator import CoherenceEvaluatorWrapper
from evaluators.fluency_evaluator import FluencyEvaluatorWrapper
from evaluators.qa_evaluator import QAEvaluatorWrapper
from azure.ai.evaluation import AzureOpenAIModelConfiguration

def load_evaluation_data(file_path):
    """Load evaluation data from JSONL file."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def main():
    # Set up model configuration
    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=os.environ["AZURE_ENDPOINT"],
        api_key=os.environ.get("AZURE_API_KEY"),
        azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
        api_version=os.environ.get("AZURE_API_VERSION"),
    )

    # Initialize evaluators
    coherence_eval = CoherenceEvaluatorWrapper(model_config=model_config, threshold=3)
    fluency_eval = FluencyEvaluatorWrapper(model_config=model_config, threshold=3)
    qa_eval = QAEvaluatorWrapper(model_config=model_config, threshold=3)

    # Load data
    data_file = "data/eval-input-complete.jsonl"
    evaluation_data = load_evaluation_data(data_file)

    # Run evaluations on first 5 entries
    for i, item in enumerate(evaluation_data[:5]):
        print(f"\n--- Evaluation {i+1} ---")
        query = item.get('query', '')
        response = item.get('response', '')
        ground_truth = item.get('ground_truth', '')
        context = item.get('context', '')  # Use context from data

        # Coherence
        coh_result = coherence_eval.evaluate(query=query, response=response)
        print(f"Coherence: {coh_result.get('coherence')} ({coh_result.get('coherence_result')})")

        # Fluency
        flu_result = fluency_eval.evaluate(response=response)
        print(f"Fluency: {flu_result.get('fluency')} ({flu_result.get('fluency_result')})")

        # QA
        qa_result = qa_eval.evaluate(query=query, context=context, response=response, ground_truth=ground_truth)
        print(f"QA F1 Score: {qa_result.get('f1_score')} ({qa_result.get('f1_result')})")

if __name__ == "__main__":
    main()