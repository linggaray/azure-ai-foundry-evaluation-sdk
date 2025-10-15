from azure.ai.evaluation import CoherenceEvaluator

class CoherenceEvaluatorWrapper:
    """
    Wrapper for Azure AI Evaluation SDK's CoherenceEvaluator.
    Evaluates the coherence of a response.
    """
    def __init__(self, model_config, threshold=3):
        self.evaluator = CoherenceEvaluator(model_config=model_config, threshold=threshold)

    def evaluate(self, query, response):
        """
        Evaluate coherence of the given response.

        Args:
            query (str): The query or question.
            response (str): The response text to evaluate.

        Returns:
            dict: Evaluation result containing coherence score and details.
        """
        return self.evaluator(query=query, response=response)