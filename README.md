# Azure AI Foundry Evaluation SDK Project

This project demonstrates how to evaluate AI model responses using the Azure AI Foundry Evaluation SDK, focusing on general-purpose evaluators: Coherence, Fluency, and QA (Question Answering).

## Prerequisites

- Python 3.8 or higher
- Azure subscription with access to Azure AI Foundry
- Azure AI Project set up

## Setup

### 1. Create and Activate Python Environment

Create a virtual environment to isolate dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### 2. Install Dependencies

Install the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

You need to set the Azure OpenAI model configuration variables:

```bash
export AZURE_ENDPOINT="your-azure-endpoint"
export AZURE_API_KEY="your-api-key"
export AZURE_DEPLOYMENT_NAME="your-deployment-name"
export AZURE_API_VERSION="your-api-version"
```

These are required for the evaluators to work.

### 4. Run the Evaluation

Execute the evaluation script to run the evaluators on the data:

```bash
python run_evaluation.py
```

This will load the data from `data/eval-input-complete.jsonl` and run Coherence, Fluency, and QA evaluations on the first 5 entries, printing the results.

### 5. Run the Tests

To run the unit tests for the evaluators:

```bash
pytest tests/
```

To run tests with verbose output and print statements (to see evaluation results):

```bash
pytest -s -v tests/
```

This will test the evaluator wrappers using the configured Azure OpenAI model and display detailed output including the evaluation results.

## Data Format

The evaluation data is stored in `data/eval-input-complete.jsonl` as JSON Lines. Each line contains:
- `id`: Unique identifier
- `query`: The input question/query
- `response`: The AI model's response
- `ground_truth`: The expected correct answer (for QA evaluation)
- Other metadata

## Evaluators Used

- **CoherenceEvaluator**: Measures how logically consistent and coherent the response is.
- **FluencyEvaluator**: Assesses the grammatical correctness and natural flow of the language.
- **QAEvaluator**: Evaluates the accuracy of the answer compared to the ground truth for question-answering tasks.

## Customization

- To evaluate more data, modify the slice in `evaluate.py` (e.g., change `evaluation_data[:10]` to `evaluation_data`).
- Add more evaluators or customize the output as needed.

## Troubleshooting

- Ensure your Azure credentials are correctly configured and you have permissions for the AI project.
- If you encounter import errors, verify that all dependencies are installed.
- Check the Azure AI Foundry documentation for the latest SDK updates.