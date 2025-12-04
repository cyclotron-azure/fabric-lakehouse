<#
.SYNOPSIS
    Setup script for Fabric Lakehouse environment (Mock Mode)
    
.DESCRIPTION
    Creates a Lakehouse in Microsoft Fabric workspace and uploads sample CSV files.
    This is a MOCK script for interview purposes - actual API calls are commented out.
    Assumes Fabric workspace already exists.
    
.PARAMETER WorkspaceName
    Name of the Fabric workspace (default: "InterviewWorkspace")
    
.PARAMETER LakehouseName
    Name of the Lakehouse to create (default: "RetailLakehouse")
    
.EXAMPLE
    .\setup-lakehouse.ps1 -WorkspaceName "MyWorkspace" -LakehouseName "RetailData"
#>

param(
    [string]$WorkspaceName = "InterviewWorkspace",
    [string]$LakehouseName = "RetailLakehouse"
)

# Configuration
$ErrorActionPreference = "Stop"
$dataPath = Join-Path $PSScriptRoot "..\data"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fabric Lakehouse Setup (Mock Mode)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify prerequisites
Write-Host "[1/5] Verifying prerequisites..." -ForegroundColor Yellow
Write-Host "  ✓ Workspace: $WorkspaceName" -ForegroundColor Green
Write-Host "  ✓ Lakehouse: $LakehouseName" -ForegroundColor Green

# Mock: Check if Azure CLI is installed
# Uncomment for real deployment:
# try {
#     $azVersion = az version --query '"azure-cli"' -o tsv
#     Write-Host "  ✓ Azure CLI installed: $azVersion" -ForegroundColor Green
# } catch {
#     Write-Error "Azure CLI not found. Install from: https://aka.ms/installazurecli"
#     exit 1
# }

Write-Host "  ✓ Azure CLI check (mocked)" -ForegroundColor Green

# Step 2: Authenticate to Fabric
Write-Host ""
Write-Host "[2/5] Authenticating to Fabric..." -ForegroundColor Yellow

# Mock: Login to Azure
# Uncomment for real deployment:
# az login --use-device-code

Write-Host "  ✓ Authentication (mocked)" -ForegroundColor Green

# Step 3: Get Workspace ID
Write-Host ""
Write-Host "[3/5] Retrieving workspace..." -ForegroundColor Yellow

# Mock: Get workspace ID via Fabric REST API
# Uncomment for real deployment:
# $token = az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv
# $headers = @{
#     "Authorization" = "Bearer $token"
#     "Content-Type" = "application/json"
# }
# $workspaceUrl = "https://api.fabric.microsoft.com/v1/workspaces?`$filter=displayName eq '$WorkspaceName'"
# $workspaceResponse = Invoke-RestMethod -Uri $workspaceUrl -Headers $headers -Method Get
# $workspaceId = $workspaceResponse.value[0].id

$workspaceId = "mock-workspace-id-12345"
Write-Host "  ✓ Workspace ID: $workspaceId" -ForegroundColor Green

# Step 4: Create Lakehouse
Write-Host ""
Write-Host "[4/5] Creating Lakehouse..." -ForegroundColor Yellow

# Mock: Create Lakehouse via Fabric REST API
# Uncomment for real deployment:
# $createLakehouseUrl = "https://api.fabric.microsoft.com/v1/workspaces/$workspaceId/lakehouses"
# $lakehouseBody = @{
#     displayName = $LakehouseName
#     description = "Retail orders lakehouse for interview assessment"
# } | ConvertTo-Json
# 
# try {
#     $lakehouseResponse = Invoke-RestMethod -Uri $createLakehouseUrl -Headers $headers -Method Post -Body $lakehouseBody
#     $lakehouseId = $lakehouseResponse.id
#     Write-Host "  ✓ Lakehouse created: $lakehouseId" -ForegroundColor Green
# } catch {
#     if ($_.Exception.Response.StatusCode -eq 409) {
#         Write-Host "  ℹ Lakehouse already exists" -ForegroundColor Yellow
#         $listUrl = "https://api.fabric.microsoft.com/v1/workspaces/$workspaceId/lakehouses?`$filter=displayName eq '$LakehouseName'"
#         $lakehouseResponse = Invoke-RestMethod -Uri $listUrl -Headers $headers -Method Get
#         $lakehouseId = $lakehouseResponse.value[0].id
#         Write-Host "  ✓ Using existing lakehouse: $lakehouseId" -ForegroundColor Green
#     } else {
#         throw
#     }
# }

$lakehouseId = "mock-lakehouse-id-67890"
Write-Host "  ✓ Lakehouse created: $lakehouseId (mocked)" -ForegroundColor Green

# Step 5: Upload CSV files
Write-Host ""
Write-Host "[5/5] Uploading CSV files..." -ForegroundColor Yellow

$csvFiles = @("customers.csv", "orders.csv")

foreach ($file in $csvFiles) {
    $filePath = Join-Path $dataPath $file
    
    if (-not (Test-Path $filePath)) {
        Write-Warning "  ⚠ File not found: $filePath"
        continue
    }
    
    # Mock: Upload file to Lakehouse Files section
    # Uncomment for real deployment:
    # $uploadUrl = "https://api.fabric.microsoft.com/v1/workspaces/$workspaceId/lakehouses/$lakehouseId/files/$file"
    # $fileContent = Get-Content $filePath -Raw -Encoding UTF8
    # $uploadHeaders = $headers.Clone()
    # $uploadHeaders["Content-Type"] = "text/csv"
    # 
    # Invoke-RestMethod -Uri $uploadUrl -Headers $uploadHeaders -Method Put -Body $fileContent
    
    Write-Host "  ✓ Uploaded: $file (mocked)" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open Fabric workspace: $WorkspaceName"
Write-Host "2. Navigate to Lakehouse: $LakehouseName"
Write-Host "3. Create a new Notebook"
Write-Host "4. Run notebooks/01_Bronze_Ingest.ipynb"
Write-Host ""
Write-Host "For real deployment, uncomment API calls in this script." -ForegroundColor Cyan
Write-Host ""

# Output connection info
$connectionInfo = @{
    WorkspaceName = $WorkspaceName
    WorkspaceId = $workspaceId
    LakehouseName = $LakehouseName
    LakehouseId = $lakehouseId
    FilesUploaded = $csvFiles
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

$connectionInfo | ConvertTo-Json | Out-File "lakehouse-connection.json"
Write-Host "Connection details saved to: lakehouse-connection.json" -ForegroundColor Green
