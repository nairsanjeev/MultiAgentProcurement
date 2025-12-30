# Azure Deployment Guide

This guide will help you deploy the Procurement Agent Demo to Azure App Service.

## Prerequisites

1. **Azure Account** - Get a free account at https://azure.microsoft.com/free/
2. **Azure CLI** - Install from https://aka.ms/installazurecli
3. **Azure Subscription** with permissions to create resources

## Quick Deployment (Automated)

Run the deployment script from the project root:

```powershell
.\deploy-azure.ps1
```

This will:
- Create a new resource group
- Create an App Service Plan
- Deploy the backend API to Azure
- Deploy the frontend web app to Azure
- Configure all settings automatically

## Manual Deployment Steps

If you prefer manual deployment or need to customize:

### 1. Login to Azure

```powershell
az login
```

### 2. Set Variables

```powershell
$RESOURCE_GROUP = "procurement-demo-rg"
$LOCATION = "eastus2"
$BACKEND_APP = "procurement-backend-<your-unique-id>"
$FRONTEND_APP = "procurement-frontend-<your-unique-id>"
$PLAN_NAME = "procurement-app-plan"
```

### 3. Create Resource Group

```powershell
az group create --name $RESOURCE_GROUP --location $LOCATION
```

### 4. Create App Service Plan

```powershell
az appservice plan create `
    --name $PLAN_NAME `
    --resource-group $RESOURCE_GROUP `
    --sku B1 `
    --is-linux
```

### 5. Deploy Backend

```powershell
# Create Web App for backend
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $PLAN_NAME `
    --name $BACKEND_APP `
    --runtime "PYTHON:3.10"

# Configure environment variables from .env file
az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP `
    --settings @backend/.env

# Set startup command
az webapp config set `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP `
    --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --timeout 120"

# Deploy code
cd backend
az webapp up `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP `
    --runtime "PYTHON:3.10"
cd ..
```

### 6. Deploy Frontend

```powershell
# Create Web App for frontend
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $PLAN_NAME `
    --name $FRONTEND_APP `
    --runtime "NODE:18-lts"

# Set backend URL
$BACKEND_URL = "https://$BACKEND_APP.azurewebsites.net"

az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $FRONTEND_APP `
    --settings `
        "NEXT_PUBLIC_API_URL=$BACKEND_URL" `
        "WEBSITE_NODE_DEFAULT_VERSION=18-lts"

# Deploy code
cd frontend
az webapp up `
    --resource-group $RESOURCE_GROUP `
    --name $FRONTEND_APP `
    --runtime "NODE:18-lts"
cd ..
```

### 7. Configure CORS

```powershell
$FRONTEND_URL = "https://$FRONTEND_APP.azurewebsites.net"

az webapp cors add `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP `
    --allowed-origins $FRONTEND_URL
```

## Post-Deployment

### Access Your Application

- **Frontend**: `https://<frontend-app>.azurewebsites.net`
- **Backend API**: `https://<backend-app>.azurewebsites.net`
- **API Docs**: `https://<backend-app>.azurewebsites.net/docs`

### Monitor Logs

```powershell
# Backend logs
az webapp log tail --name $BACKEND_APP --resource-group $RESOURCE_GROUP

# Frontend logs
az webapp log tail --name $FRONTEND_APP --resource-group $RESOURCE_GROUP
```

### View in Azure Portal

```powershell
az webapp browse --name $FRONTEND_APP --resource-group $RESOURCE_GROUP
```

## Environment Variables

The following environment variables need to be set in Azure:

### Backend (Required)
```
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT_NAME=<model-name>
FOUNDRY_PROJECT_ENDPOINT=<foundry-endpoint>
FOUNDRY_MODEL_DEPLOYMENT_NAME=<model-name>
```

### Frontend (Auto-configured)
```
NEXT_PUBLIC_API_URL=<backend-url>
```

## Scaling

### Scale Up (Vertical)

```powershell
az appservice plan update `
    --name $PLAN_NAME `
    --resource-group $RESOURCE_GROUP `
    --sku P1V2
```

### Scale Out (Horizontal)

```powershell
az appservice plan update `
    --name $PLAN_NAME `
    --resource-group $RESOURCE_GROUP `
    --number-of-workers 3
```

## Troubleshooting

### Backend not starting

1. Check logs: `az webapp log tail --name $BACKEND_APP --resource-group $RESOURCE_GROUP`
2. Verify environment variables are set
3. Ensure gunicorn is in requirements.txt
4. Check startup command is correct

### Frontend not loading

1. Check logs: `az webapp log tail --name $FRONTEND_APP --resource-group $RESOURCE_GROUP`
2. Verify NEXT_PUBLIC_API_URL is set correctly
3. Check CORS configuration on backend
4. Verify Node.js version (18-lts)

### CORS errors

```powershell
az webapp cors add `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP `
    --allowed-origins "https://<frontend-app>.azurewebsites.net"
```

### 502 Bad Gateway

- App is starting up (wait 1-2 minutes)
- Check startup command
- Review application logs

## Cost Optimization

### Development/Testing
- Use **B1** (Basic) tier: ~$13/month per app
- Stop apps when not in use: `az webapp stop --name <app-name> --resource-group <rg>`

### Production
- Use **P1V2** (Premium) tier: ~$73/month per app
- Includes auto-scaling, staging slots, custom domains

### Delete Resources

When done testing:

```powershell
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## CI/CD (Optional)

### GitHub Actions

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Deploy Backend
        uses: azure/webapps-deploy@v2
        with:
          app-name: '<backend-app-name>'
          package: './backend'

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Deploy Frontend
        uses: azure/webapps-deploy@v2
        with:
          app-name: '<frontend-app-name>'
          package: './frontend'
```

## Security Best Practices

1. **Use Managed Identity** instead of API keys where possible
2. **Enable HTTPS only**: `az webapp update --https-only true`
3. **Restrict CORS** to specific domains (not "*")
4. **Use Azure Key Vault** for sensitive configuration
5. **Enable Application Insights** for monitoring

## Support

For issues:
1. Check Azure Portal logs
2. Review deployment script output
3. Verify all environment variables
4. Check service health in Azure Portal

## Additional Resources

- [Azure App Service Documentation](https://learn.microsoft.com/azure/app-service/)
- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)
- [Python on Azure](https://learn.microsoft.com/azure/developer/python/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
