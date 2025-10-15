from azure.ai.evaluation import QAEvaluator

class QAEvaluatorWrapper:
    """
    Wrapper for Azure AI Evaluation SDK's QAEvaluator.
    Evaluates the quality of answers for question-answering tasks.
    """
    def __init__(self, model_config, threshold=3):
        self.evaluator = QAEvaluator(model_config=model_config, threshold=threshold)

    def evaluate(self, query, context, response, ground_truth):
        """
        Evaluate QA quality of the given answer.

        Args:
            query (str): The question asked.
            context (str): The context information.
            response (str): The answer provided.
            ground_truth (str): The correct ground truth answer.

        Returns:
            dict: Evaluation result containing QA scores and details.
        """
        return self.evaluator(query=query, context=context, response=response, ground_truth=ground_truth)