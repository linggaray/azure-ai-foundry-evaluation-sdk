from azure.ai.evaluation import FluencyEvaluator

class FluencyEvaluatorWrapper:
    """
    Wrapper for Azure AI Evaluation SDK's FluencyEvaluator.
    Evaluates the fluency of a response.
    """
    def __init__(self, model_config, threshold=3):
        self.evaluator = FluencyEvaluator(model_config=model_config, threshold=threshold)

    def evaluate(self, response):
        """
        Evaluate fluency of the given response.

        Args:
            response (str): The response text to evaluate.

        Returns:
            dict: Evaluation result containing fluency score and details.
        """
        return self.evaluator(response=response)