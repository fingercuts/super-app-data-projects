# SwiftHub Data Platform: Setup Script for Windows (PowerShell)

Write-Host "🚀 Starting local environment setup..." -ForegroundColor Cyan

# 1. Create virtual environment natively
if (-Not (Test-Path -Path ".venv")) {
    Write-Host "📦 Creating virtual environment..."
    python -m venv .venv
}

# 2. Activate virtual environment natively
Write-Host "🔌 Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

# 3. Upgrade pip natively
Write-Host "🆙 Upgrading pip..."
python -m pip install --upgrade pip

# 4. Install requirements natively
Write-Host "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 5. Initialize dbt dependencies natively
Write-Host "🛠️ Initializing dbt packages..."
cd dbt_project
dbt deps
cd ..

Write-Host "✅ Setup complete! The SwiftHub Architecture is ready to execute." -ForegroundColor Green
Write-Host "To start, run: .\.venv\Scripts\Activate.ps1"
