# Azure Deployment Script for Procurement Agent Demo
# This script deploys both backend and frontend to Azure App Service

Write-Host "🚀 Deploying Procurement Agent Demo to Azure..." -ForegroundColor Cyan

# Configuration
$RESOURCE_GROUP = "procurement-demo-rg"
$LOCATION = "eastus2"
$BACKEND_APP = "procurement-backend-app"
$FRONTEND_APP = "procurement-frontend-app"
$PLAN_NAME = "procurement-app-plan"

# Check if Azure CLI is installed
if (!(Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Azure CLI is not installed. Please install it from https://aka.ms/installazurecli" -ForegroundColor Red
    exit 1
}

# Login check
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
$account = az account show 2>$null | ConvertFrom-Json
if (!$account) {
    Write-Host "Please login to Azure..." -ForegroundColor Yellow
    az login
}

Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
Write-Host "   Subscription: $($account.name)" -ForegroundColor Green

# Create Resource Group
Write-Host "`n📦 Creating resource group: $RESOURCE_GROUP..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION --output none
Write-Host "✅ Resource group created" -ForegroundColor Green

# Create App Service Plan (Linux with Python support)
Write-Host "`n📋 Creating App Service Plan: $PLAN_NAME..." -ForegroundColor Yellow
az appservice plan create `
    --name $PLAN_NAME `
    --resource-group $RESOURCE_GROUP `
    --sku B1 `
    --is-linux `
    --output none
Write-Host "✅ App Service Plan created" -ForegroundColor Green

# Create Backend Web App
Write-Host "`n🔧 Creating Backend Web App: $BACKEND_APP..." -ForegroundColor Yellow
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $PLAN_NAME `
    --name $BACKEND_APP `
    --runtime "PYTHON:3.10" `
    --output none

# Configure Backend App Settings
Write-Host "⚙️  Configuring backend settings..." -ForegroundColor Yellow

# Read .env file and set as app settings
$envVars = @{}
Get-Content "backend\.env" | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

# Add WEBSITE_STARTUP_COMMAND
$envVars["WEBSITE_STARTUP_COMMAND"] = "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --timeout 120"
$envVars["SCM_DO_BUILD_DURING_DEPLOYMENT"] = "true"
$envVars["ENABLE_ORYX_BUILD"] = "true"

# Convert to app settings format
$settingsArray = @()
foreach ($key in $envVars.Keys) {
    $settingsArray += "$key=$($envVars[$key])"
}

az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP `
    --settings $settingsArray `
    --output none

Write-Host "✅ Backend configured" -ForegroundColor Green

# Deploy Backend
Write-Host "`n📤 Deploying backend code..." -ForegroundColor Yellow
Push-Location backend
az webapp up `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP `
    --runtime "PYTHON:3.10" `
    --sku B1 `
    --output none
Pop-Location
Write-Host "✅ Backend deployed" -ForegroundColor Green

$BACKEND_URL = "https://$BACKEND_APP.azurewebsites.net"
Write-Host "   Backend URL: $BACKEND_URL" -ForegroundColor Cyan

# Create Frontend Web App
Write-Host "`n🎨 Creating Frontend Web App: $FRONTEND_APP..." -ForegroundColor Yellow
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $PLAN_NAME `
    --name $FRONTEND_APP `
    --runtime "NODE:18-lts" `
    --output none

# Configure Frontend App Settings
Write-Host "⚙️  Configuring frontend settings..." -ForegroundColor Yellow

# Update frontend .env.local with backend URL
$frontendEnv = @"
NEXT_PUBLIC_API_URL=$BACKEND_URL
"@
Set-Content "frontend\.env.production" $frontendEnv

az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $FRONTEND_APP `
    --settings `
        "NEXT_PUBLIC_API_URL=$BACKEND_URL" `
        "WEBSITE_NODE_DEFAULT_VERSION=18-lts" `
        "SCM_DO_BUILD_DURING_DEPLOYMENT=true" `
    --output none

Write-Host "✅ Frontend configured" -ForegroundColor Green

# Deploy Frontend
Write-Host "`n📤 Deploying frontend code..." -ForegroundColor Yellow
Push-Location frontend
az webapp up `
    --resource-group $RESOURCE_GROUP `
    --name $FRONTEND_APP `
    --runtime "NODE:18-lts" `
    --sku B1 `
    --output none
Pop-Location
Write-Host "✅ Frontend deployed" -ForegroundColor Green

$FRONTEND_URL = "https://$FRONTEND_APP.azurewebsites.net"

# Enable CORS on backend
Write-Host "`n🔐 Configuring CORS..." -ForegroundColor Yellow
az webapp cors add `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP `
    --allowed-origins $FRONTEND_URL `
    --output none
Write-Host "✅ CORS configured" -ForegroundColor Green

# Summary
Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Application URLs:" -ForegroundColor Cyan
Write-Host "   Frontend: $FRONTEND_URL" -ForegroundColor White
Write-Host "   Backend:  $BACKEND_URL" -ForegroundColor White
Write-Host ""
Write-Host "📊 Azure Portal:" -ForegroundColor Cyan
Write-Host "   https://portal.azure.com/#@/resource/subscriptions/$($account.id)/resourceGroups/$RESOURCE_GROUP" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Manage your apps:" -ForegroundColor Cyan
Write-Host "   Backend:  https://portal.azure.com/#@/resource/subscriptions/$($account.id)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$BACKEND_APP" -ForegroundColor White
Write-Host "   Frontend: https://portal.azure.com/#@/resource/subscriptions/$($account.id)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$FRONTEND_APP" -ForegroundColor White
Write-Host ""
Write-Host "💡 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Open $FRONTEND_URL in your browser" -ForegroundColor White
Write-Host "   2. Test the procurement workflow" -ForegroundColor White
Write-Host "   3. Monitor logs: az webapp log tail --name $BACKEND_APP --resource-group $RESOURCE_GROUP" -ForegroundColor White
Write-Host ""
Write-Host "🗑️  To delete all resources:" -ForegroundColor Red
Write-Host "   az group delete --name $RESOURCE_GROUP --yes --no-wait" -ForegroundColor White
Write-Host ""
