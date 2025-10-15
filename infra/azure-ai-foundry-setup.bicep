param location string = 'EastUS2'
param hubName string
param ownerTag string

resource aiFoundry 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: hubName
  location: location
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: hubName
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
  tags: {
    owner: ownerTag
  }
}

resource gpt4oDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: aiFoundry
  name: 'gpt-4o'
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-08-06'
    }
  }
}

output aiFoundryName string = aiFoundry.name
output aiFoundryEndpoint string = aiFoundry.properties.endpoint
output gpt4oDeploymentName string = gpt4oDeployment.name