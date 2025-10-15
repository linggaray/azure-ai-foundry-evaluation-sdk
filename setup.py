from setuptools import setup, find_packages

setup(
    name="azure-ai-foundry-evaluation-sdk",
    version="0.1.0",
    description="A Python project for evaluating AI models using Azure AI Foundry Evaluation SDK",
    packages=find_packages(),
    install_requires=[
        "azure-ai-evaluation",
        "azure-identity",
        "azure-ai-projects",
        "azure-ai-ml",
        "pandas"
    ],
)