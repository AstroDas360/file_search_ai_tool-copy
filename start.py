#!/usr/bin/env python
"""
Startup script for Document Search AI Tool
Checks prerequisites before starting the server
"""

import sys
import os

print("=" * 70)
print("Document Search AI Tool - Starting Up")
print("=" * 70)

# Check 1: Python version
print("\n[1/5] Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    print(f"   ✗ Python 3.8+ required, found {sys.version_info.major}.{sys.version_info.minor}")
    sys.exit(1)

# Check 2: Dependencies
print("\n[2/5] Checking dependencies...")
required_packages = [
    'flask',
    'flask_cors', 
    'openai',
    'numpy',
    'sklearn',
    'PyPDF2',
    'docx',
    'bs4'
]

missing = []
for package in required_packages:
    try:
        __import__(package)
        print(f"   ✓ {package}")
    except ImportError:
        missing.append(package)
        print(f"   ✗ {package} - NOT FOUND")

if missing:
    print(f"\n   Missing packages: {', '.join(missing)}")
    print("   Install with: pip install -r requirements.txt")
    sys.exit(1)

# Check 3: Configuration
print("\n[3/5] Checking configuration...")
try:
    import config
    
    if hasattr(config, 'OPENAI_API_KEY'):
        if config.OPENAI_API_KEY and config.OPENAI_API_KEY != "your_openai_api_key_here":
            print("   ✓ OpenAI API key configured")
        else:
            print("   ⚠  OpenAI API key not set")
            print("   Create .env file with: OPENAI_API_KEY=your_key_here")
            
            response = input("\n   Continue anyway? (y/n): ")
            if response.lower() != 'y':
                print("   Startup cancelled. Please configure API key.")
                sys.exit(0)
    else:
        print("   ✗ Configuration error: OPENAI_API_KEY not found")
        sys.exit(1)
        
    print(f"   ✓ Upload folder: {config.UPLOAD_FOLDER}")
    print(f"   ✓ Embeddings folder: {config.EMBEDDINGS_FOLDER}")
    
except Exception as e:
    print(f"   ✗ Configuration error: {e}")
    sys.exit(1)

# Check 4: Directories
print("\n[4/5] Checking data directories...")
try:
    import config
    
    for dir_path in [config.UPLOAD_FOLDER, config.EMBEDDINGS_FOLDER]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"   ✓ Created: {dir_path}")
        else:
            print(f"   ✓ Exists: {dir_path}")
            
except Exception as e:
    print(f"   ✗ Directory error: {e}")
    sys.exit(1)

# Check 5: Import application
print("\n[5/5] Loading application...")
try:
    from api import app, init_app
    print("   ✓ Application loaded successfully")
except Exception as e:
    print(f"   ✗ Failed to load application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# All checks passed
print("\n" + "=" * 70)
print("✅ All checks passed! Starting server...")
print("=" * 70)
print("\n🌐 Open your browser to: http://localhost:5001")
print("📁 Upload page: http://localhost:5001/upload")
print("\n💡 Tips:")
print("   - Upload documents on the Upload page")
print("   - Search using natural language")
print("   - Generate AI summaries for explanations")
print("\n🛑 Press Ctrl+C to stop the server")
print("=" * 70 + "\n")

# Start the server
if __name__ == '__main__':
    import config
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.API_DEBUG
    )
