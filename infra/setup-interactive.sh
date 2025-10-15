#!/bin/bash

set -e

echo "Checking Azure login status..."
if az account show > /dev/null 2>&1; then
  echo "Already logged in to Azure."
else
  echo "Not logged in. Initiating Azure login..."
  az login
  echo "Login completed."
fi

echo "Listing available subscriptions:"
az account list --output table

read -p "Enter the number of the subscription to use (1-based): " sub_num

# Get number of subscriptions
subscriptions=$(az account list --query 'length(@)' -o tsv)

if [ "$sub_num" -lt 1 ] || [ "$sub_num" -gt "$subscriptions" ]; then
  echo "Invalid subscription number. Please enter a number between 1 and $subscriptions."
  exit 1
fi

index=$((sub_num - 1))
sub_id=$(az account list --query "[$index].id" -o tsv)
az account set --subscription $sub_id

echo "Subscription set to: $(az account show --query 'name' -o tsv)"

read -p "Enter Resource Group name: " rg_name

read -p "Enter Owner tag: " owner_tag

read -p "Enter Azure AI Foundry Hub name: " hub_name

echo "Creating resource group '$rg_name' in East US 2 with owner tag '$owner_tag'..."
az group create --name $rg_name --location eastus2 --tags owner=$owner_tag

echo "Deploying Azure AI Foundry Hub and GPT-4o..."
az deployment group create \
  --resource-group $rg_name \
  --template-file azure-ai-foundry-setup.bicep \
  --parameters hubName=$hub_name location=eastus2 ownerTag=$owner_tag \
  --mode Incremental \
  --verbose

if [ $? -eq 0 ]; then
  echo "Deployment completed successfully!"
  echo "Getting deployment outputs..."
  az deployment group show --resource-group $rg_name --name azure-ai-foundry-setup --query properties.outputs
  
  echo ""
  echo "=================================================="
  echo "Retrieving configuration details..."
  echo "=================================================="
  
  # Get endpoint from deployment outputs
  endpoint=$(az deployment group show --resource-group $rg_name --name azure-ai-foundry-setup --query 'properties.outputs.aiFoundryEndpoint.value' -o tsv)
  deployment_name=$(az deployment group show --resource-group $rg_name --name azure-ai-foundry-setup --query 'properties.outputs.gpt4oDeploymentName.value' -o tsv)
  ai_foundry_name=$(az deployment group show --resource-group $rg_name --name azure-ai-foundry-setup --query 'properties.outputs.aiFoundryName.value' -o tsv)
  
  # Get API key
  echo "Retrieving API key..."
  api_key=$(az cognitiveservices account keys list --name $ai_foundry_name --resource-group $rg_name --query 'key1' -o tsv)
  
  # Get subscription ID
  subscription_id=$(az account show --query 'id' -o tsv)
  
  echo ""
  echo "=================================================="
  echo "Configuration Retrieved Successfully!"
  echo "=================================================="
  echo ""
  echo "AZURE_OPENAI_ENDPOINT=$endpoint"
  echo "AZURE_OPENAI_DEPLOYMENT_NAME=$deployment_name"
  echo "AZURE_OPENAI_API_VERSION=2024-12-01-preview"
  echo "AZURE_OPENAI_API_KEY=$api_key"
  echo ""
  echo "AZURE_SUBSCRIPTION_ID=$subscription_id"
  echo "AZURE_RESOURCE_GROUP=$rg_name"
  echo "AZURE_PROJECT_NAME=$ai_foundry_name"
  echo ""
  
  # Create .env file
  env_file="../.env"
  echo "Creating .env file at $env_file..."
  
  cat > $env_file << EOF
# Azure OpenAI Configuration (for RAG, General Purpose, and Agentic evaluators)
AZURE_OPENAI_ENDPOINT=$endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=$deployment_name
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_API_KEY=$api_key

# Azure AI Foundry Project Configuration (for Risk/Safety evaluators)
# Hub and Project created in East US 2 for full evaluator support
AZURE_SUBSCRIPTION_ID=$subscription_id
AZURE_RESOURCE_GROUP=$rg_name
AZURE_PROJECT_NAME=$ai_foundry_name
EOF
  
  echo ""
  echo "✅ .env file created successfully at: $env_file"
  echo ""
  echo "=================================================="
  echo "🎉 Setup Complete!"
  echo "=================================================="
  echo ""
  echo "Your Azure AI Foundry Hub is ready to use!"
  echo "All configuration has been saved to .env file."
  echo ""
  echo "Resource Group: $rg_name"
  echo "AI Foundry Hub: $ai_foundry_name"
  echo "Endpoint: $endpoint"
  echo "Deployment: $deployment_name"
  echo ""
else
  echo "Deployment failed. Check the error messages above."
  exit 1
fi