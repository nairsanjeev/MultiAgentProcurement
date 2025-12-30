# Deployment Guide

## Production Deployment Considerations

This guide covers deploying the Procurement Agent system to production environments.

## Backend Deployment

### Option 1: Azure App Service (Recommended)

1. **Create Azure App Service:**
```bash
az webapp create \
  --resource-group your-rg \
  --plan your-app-service-plan \
  --name procurement-agent-api \
  --runtime "PYTHON:3.11"
```

2. **Configure Application Settings:**
```bash
az webapp config appsettings set \
  --name procurement-agent-api \
  --resource-group your-rg \
  --settings \
    AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
    AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o" \
    FOUNDRY_PROJECT_ENDPOINT="https://your-project.cognitiveservices.azure.com/" \
    USE_AZURE_CREDENTIAL="true"
```

3. **Enable Managed Identity:**
```bash
az webapp identity assign \
  --name procurement-agent-api \
  --resource-group your-rg
```

4. **Deploy Code:**
```bash
cd backend
zip -r deploy.zip .
az webapp deployment source config-zip \
  --resource-group your-rg \
  --name procurement-agent-api \
  --src deploy.zip
```

### Option 2: Azure Container Instances

1. **Create Dockerfile:**
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --pre

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and Push:**
```bash
docker build -t procurement-agent-api:latest .
docker tag procurement-agent-api:latest your-acr.azurecr.io/procurement-agent-api:latest
docker push your-acr.azurecr.io/procurement-agent-api:latest
```

3. **Deploy Container:**
```bash
az container create \
  --resource-group your-rg \
  --name procurement-agent-api \
  --image your-acr.azurecr.io/procurement-agent-api:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --environment-variables \
    AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
    AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o"
```

## Frontend Deployment

### Option 1: Azure Static Web Apps (Recommended)

1. **Install Azure Static Web Apps CLI:**
```bash
npm install -g @azure/static-web-apps-cli
```

2. **Build for Production:**
```bash
cd frontend
npm run build
```

3. **Deploy:**
```bash
swa deploy \
  --app-location frontend \
  --output-location .next \
  --resource-group your-rg \
  --app-name procurement-agent-frontend
```

4. **Configure Environment Variables:**
   - Go to Azure Portal → Static Web Apps → Configuration
   - Add: `NEXT_PUBLIC_API_URL=https://your-api-url.azurewebsites.net`

### Option 2: Vercel

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Deploy:**
```bash
cd frontend
vercel --prod
```

3. **Set Environment Variables:**
```bash
vercel env add NEXT_PUBLIC_API_URL production
```

## Security Considerations

### 1. Authentication & Authorization
- Implement Azure AD authentication
- Add API key management
- Use role-based access control (RBAC)

### 2. API Security
- Enable HTTPS only
- Implement rate limiting
- Add request validation
- Use Azure API Management

### 3. Data Protection
- Encrypt sensitive data at rest
- Use Azure Key Vault for secrets
- Implement data retention policies
- Add audit logging

### 4. Network Security
- Use Azure Virtual Network
- Configure network security groups
- Enable Azure DDoS Protection
- Use Azure Front Door for WAF

## Monitoring & Logging

### Application Insights

1. **Add to Backend:**
```python
# pip install opencensus-ext-azure
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=your-key'
))
```

2. **Add to Frontend:**
```typescript
// npm install @microsoft/applicationinsights-web
import { ApplicationInsights } from '@microsoft/applicationinsights-web';

const appInsights = new ApplicationInsights({
  config: {
    instrumentationKey: 'your-key'
  }
});
appInsights.loadAppInsights();
```

### Health Checks

Configure health check endpoints:
- Backend: `https://your-api.azurewebsites.net/health`
- Set up Azure Monitor alerts for failures

## Scaling Configuration

### Backend Scaling
```bash
az appservice plan update \
  --name your-plan \
  --resource-group your-rg \
  --sku P1V2

az webapp config set \
  --name procurement-agent-api \
  --resource-group your-rg \
  --always-on true \
  --auto-heal-enabled true
```

### Database for Production

Add Azure Cosmos DB or Azure SQL for persistence:

```python
# Example with Cosmos DB
from azure.cosmos import CosmosClient

client = CosmosClient(url, credential)
database = client.get_database_client("procurement")
container = database.get_container_client("purchase_orders")
```

## CI/CD Pipeline

### Azure DevOps Pipeline

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Backend
    jobs:
      - job: BuildBackend
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.11'
          - script: |
              cd backend
              pip install -r requirements.txt --pre
              python -m pytest
            displayName: 'Test Backend'
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'your-subscription'
              appName: 'procurement-agent-api'
              package: 'backend'

  - stage: Frontend
    jobs:
      - job: BuildFrontend
        steps:
          - task: NodeTool@0
            inputs:
              versionSpec: '18.x'
          - script: |
              cd frontend
              npm install
              npm run build
            displayName: 'Build Frontend'
          - task: AzureStaticWebApp@0
            inputs:
              app_location: 'frontend'
              output_location: '.next'
```

## Cost Optimization

### 1. Model Selection
- Use **gpt-4o-mini** for non-critical analyses
- Use **gpt-4o** only for complex extraction
- Implement caching for repeated queries

### 2. Resource Optimization
- Use Azure Spot Instances for dev/test
- Implement auto-scaling rules
- Use Azure Reserved Instances for production

### 3. Monitoring Costs
- Set up Azure Cost Management alerts
- Monitor token usage in Application Insights
- Implement request throttling

## Backup & Disaster Recovery

1. **Database Backups:**
   - Enable automated backups
   - Configure geo-replication
   - Test restore procedures

2. **Configuration Backups:**
   - Store configuration in Azure Key Vault
   - Version control all infrastructure as code
   - Document recovery procedures

## Compliance & Governance

- Enable Azure Policy
- Configure compliance reports
- Implement data residency requirements
- Add audit trails
- Configure retention policies

## Post-Deployment Checklist

- [ ] Health checks passing
- [ ] SSL/TLS certificates configured
- [ ] Environment variables set
- [ ] Monitoring and alerts configured
- [ ] Backup procedures tested
- [ ] Security scan completed
- [ ] Load testing performed
- [ ] Documentation updated
- [ ] Disaster recovery plan documented
- [ ] Team trained on operations

---

For production support, refer to:
- [Azure App Service Documentation](https://learn.microsoft.com/azure/app-service/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
