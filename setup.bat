@echo off
echo 🚀 IoT Protocol Comparison Setup for Windows
echo Real LwM2M vs Real rs-matter Implementation
echo ==========================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%

:: Check if Rust is installed
cargo --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Rust not found. Installing Rust...
    echo Please download and install Rust from: https://rustup.rs/
    echo After installation, restart this script
    pause
    start https://rustup.rs/
    exit /b 1
)

:: Check Rust version
for /f "tokens=2" %%i in ('cargo --version 2^>^&1') do set RUST_VERSION=%%i
echo ✅ Rust found: %RUST_VERSION%

:: Create virtual environment
echo 🔧 Setting up Python environment...
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

:: Upgrade pip
python -m pip install --upgrade pip

:: Install Python dependencies
echo 📦 Installing Python dependencies...
pip install aiocoap matplotlib seaborn pandas numpy scipy cbor2 cryptography python-dateutil

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

:: Create project directories
echo 📁 Creating project structure...
if not exist lwm2m-project mkdir lwm2m-project
if not exist matter-project mkdir matter-project
if not exist analysis mkdir analysis
if not exist results mkdir results
if not exist results\charts mkdir results\charts
if not exist results\data mkdir results\data
if not exist results\reports mkdir results\reports
if not exist docs mkdir docs

:: Build Matter analyzer
echo 🦀 Building Matter analyzer...
cd matter-project

:: Check if Cargo.toml exists
if not exist Cargo.toml (
    echo ❌ Cargo.toml not found in matter-project directory
    echo Please ensure all project files are in place
    pause
    exit /b 1
)

:: Build the project
cargo build --release
if %errorlevel% neq 0 (
    echo ❌ Matter analyzer build failed
    echo Check the error messages above
    pause
    exit /b 1
)

echo ✅ Matter analyzer built successfully
cd ..

:: Create activation script for Windows
echo @echo off > activate_env.bat
echo call venv\Scripts\activate.bat >> activate_env.bat
echo echo ✅ Environment activated (Windows) >> activate_env.bat
echo echo 🚀 Ready to run: python run_analysis.py >> activate_env.bat

echo.
echo ==================================================
echo 🎉 SETUP COMPLETE!
echo ==================================================
echo.
echo 📁 Project Structure:
echo    ✅ Python virtual environment: venv\
echo    ✅ LwM2M implementation: lwm2m-project\
echo    ✅ Matter implementation: matter-project\
echo    ✅ Analysis framework: analysis\
echo    ✅ Results directory: results\
echo.
echo 🚀 Ready to Run:
echo    1. Activate environment: activate_env.bat
echo    2. Run analysis: python run_analysis.py
echo    3. View results: explorer results\charts\
echo.
echo ⚡ Estimated analysis runtime: 2-5 minutes
echo 📊 Expected output: 6 charts + data files + report
echo.
echo ==================================================

pause