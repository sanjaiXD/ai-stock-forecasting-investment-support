import sys
import subprocess
import platform

print("=" * 70)
print("🔍 AI STOCK FORECASTING - SYSTEM DIAGNOSTIC TOOL")
print("=" * 70)
print()

# Check Python version
print("1️⃣  Checking Python version...")
python_version = sys.version_info
print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
    print("   ⚠️  WARNING: Python 3.8+ is recommended")
else:
    print("   ✅ Version OK")
print()

# Check platform
print("2️⃣  Checking Operating System...")
print(f"   System: {platform.system()}")
print(f"   Release: {platform.release()}")
print(f"   Architecture: {platform.machine()}")
print()

# Check pip
print("3️⃣  Checking pip...")
try:
    result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                          capture_output=True, text=True)
    print(f"   ✅ {result.stdout.strip()}")
except Exception as e:
    print(f"   ❌ pip not found: {e}")
print()

# Check required packages
print("4️⃣  Checking installed packages...")
required_packages = [
    'flask',
    'numpy',
    'pandas',
    'sklearn',
    'tensorflow',
    'yfinance',
    'matplotlib',
    'seaborn'
]

installed = []
missing = []

for package in required_packages:
    try:
        __import__(package)
        installed.append(package)
        print(f"   ✅ {package}")
    except ImportError:
        missing.append(package)
        print(f"   ❌ {package} - NOT INSTALLED")

print()

# Check project structure
print("5️⃣  Checking project files...")
import os

required_files = [
    'app.py',
    'requirements.txt',
    'model/__init__.py',
    'model/train_model.py',
    'model/predict.py',
    'static/style.css',
    'static/script.js',
    'templates/index.html'
]

files_ok = True
for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - MISSING")
        files_ok = False

print()

# Summary
print("=" * 70)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 70)

if missing:
    print(f"❌ Missing packages: {', '.join(missing)}")
    print()
    print("To install missing packages, run:")
    print("   pip install -r requirements.txt")
else:
    print("✅ All required packages are installed!")

if not files_ok:
    print("❌ Some project files are missing!")
    print("   Please re-extract the project ZIP file")
else:
    print("✅ All project files are present!")

print()

if not missing and files_ok:
    print("🎉 SYSTEM READY! You can run the application with:")
    print("   python app.py")
else:
    print("⚠️  Please fix the issues above before running the application")

print("=" * 70)
