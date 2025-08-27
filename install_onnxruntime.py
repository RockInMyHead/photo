#!/usr/bin/env python3
"""
Smart installer for ONNXRuntime with fallback options
"""

import subprocess
import sys
import platform

def run_command(cmd, description):
    """Run command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def install_onnxruntime():
    """Install ONNXRuntime with different strategies"""
    print("🚀 Installing ONNXRuntime for InsightFace")
    print("=" * 50)

    # Check Python version and architecture
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Platform: {platform.platform()}")
    print(f"🏗️ Architecture: {platform.machine()}")

    # Strategy 1: Standard onnxruntime
    print("\n📦 Strategy 1: Standard onnxruntime")
    if run_command("pip install onnxruntime", "Installing onnxruntime"):
        print("\n🎉 ONNXRuntime installed successfully!")
        return True

    # Strategy 2: CPU-only version (smaller, more compatible)
    print("\n📦 Strategy 2: CPU-only onnxruntime")
    if run_command("pip install onnxruntime-cpu", "Installing onnxruntime-cpu"):
        print("\n🎉 ONNXRuntime CPU installed successfully!")
        return True

    # Strategy 3: Specific version for compatibility
    print("\n📦 Strategy 3: Compatible version")
    if run_command("pip install onnxruntime==1.15.1", "Installing onnxruntime 1.15.1"):
        print("\n🎉 ONNXRuntime 1.15.1 installed successfully!")
        return True

    # Strategy 4: Pre-release version
    print("\n📦 Strategy 4: Pre-release version")
    if run_command("pip install --pre onnxruntime", "Installing pre-release onnxruntime"):
        print("\n🎉 Pre-release ONNXRuntime installed successfully!")
        return True

    # Strategy 5: Alternative source
    print("\n📦 Strategy 5: Alternative source")
    if run_command("pip install --upgrade --force-reinstall onnxruntime", "Force reinstall onnxruntime"):
        print("\n🎉 ONNXRuntime force-installed successfully!")
        return True

    print("\n❌ All installation strategies failed!")
    print("\n💡 Manual alternatives:")
    print("1. Try: conda install onnxruntime")
    print("2. Download from: https://onnxruntime.ai/")
    print("3. Use system package manager")
    
    return False

def install_full_insightface_deps():
    """Install all InsightFace dependencies"""
    print("\n🔧 Installing all InsightFace dependencies...")
    
    deps = [
        ("insightface", "InsightFace library"),
        ("onnxruntime", "ONNX Runtime"),
        ("hdbscan", "HDBSCAN clustering"), 
        ("scikit-learn", "Machine learning tools"),
        ("tqdm", "Progress bars")
    ]
    
    success_count = 0
    for package, description in deps:
        if run_command(f"pip install {package}", f"Installing {description}"):
            success_count += 1
    
    print(f"\n📊 Result: {success_count}/{len(deps)} packages installed")
    
    if success_count == len(deps):
        print("🎉 All InsightFace dependencies installed!")
        return True
    elif success_count >= 3:
        print("⚠️ Most dependencies installed, InsightFace might work")
        return True
    else:
        print("❌ Too many dependencies failed")
        return False

def test_imports():
    """Test if ONNXRuntime and InsightFace work"""
    print("\n🔍 Testing imports...")
    
    # Test ONNXRuntime
    try:
        import onnxruntime
        print(f"✅ ONNXRuntime {onnxruntime.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ ONNXRuntime import failed: {e}")
        return False
    
    # Test InsightFace
    try:
        import insightface
        print(f"✅ InsightFace imported successfully")
    except ImportError as e:
        print(f"⚠️ InsightFace import failed: {e}")
        print("This is normal if InsightFace wasn't installed yet")
    
    # Test other dependencies
    deps = ['sklearn', 'hdbscan', 'tqdm']
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep} imported successfully")
        except ImportError:
            print(f"⚠️ {dep} not available")
    
    return True

def main():
    print("🎯 ONNXRuntime Installer for Photo Sorter")
    print("=" * 50)
    
    # First try to install ONNXRuntime
    if install_onnxruntime():
        # Then install other InsightFace dependencies
        install_full_insightface_deps()
    
    # Test everything
    test_imports()
    
    print("\n" + "=" * 50)
    print("Installation completed!")
    print("Now try running: python main_simple.py")

if __name__ == "__main__":
    main()
