"""
Quick Start Script for Music Description Generator
Verifies installation and provides guided setup
"""

import sys
import subprocess
import os
from pathlib import Path


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("🎵 MUSIC DESCRIPTION GENERATOR - QUICK START")
    print("="*70 + "\n")


def check_python_version():
    """Verify Python version"""
    print("📋 Checking Python version...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} detected")
        print("  ERROR: Python 3.8+ required")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required = [
        'librosa',
        'soundfile',
        'numpy',
        'flask',
        'pandas',
        'transformers'
    ]
    
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            missing.append(package)
    
    return missing


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("\n🎬 Checking FFmpeg...")
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ FFmpeg is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ FFmpeg not found")
    print("\n  Install FFmpeg:")
    print("  - Windows: Download from https://ffmpeg.org/download.html")
    print("  - Mac: brew install ffmpeg")
    print("  - Linux: sudo apt-get install ffmpeg")
    return False


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")
    
    directories = [
        'uploads',
        'sample_tracks',
        'analysis_results',
        'batch_results',
        'templates'
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"✓ Created: {directory}/")
        else:
            print(f"✓ Exists: {directory}/")


def check_files():
    """Check if required Python files exist"""
    print("\n📄 Checking project files...")
    
    required_files = [
        'music_analyzer.py',
        'batch_analyzer.py',
        'app.py',
        'requirements.txt',
        'templates/index.html'
    ]
    
    missing = []
    
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing.append(file)
    
    return missing


def install_dependencies():
    """Offer to install missing dependencies"""
    print("\n📥 Installing dependencies...")
    print("This may take 5-10 minutes...")
    
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            check=True
        )
        print("\n✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ Failed to install dependencies")
        print("  Try manually: pip install -r requirements.txt")
        return False


def show_next_steps(has_dependencies, has_ffmpeg):
    """Show what to do next"""
    print("\n" + "="*70)
    print("📝 NEXT STEPS")
    print("="*70 + "\n")
    
    if not has_dependencies:
        print("1. Install Python dependencies:")
        print("   pip install -r requirements.txt")
        print()
    
    if not has_ffmpeg:
        print("2. Install FFmpeg:")
        print("   - Windows: https://ffmpeg.org/download.html")
        print("   - Mac: brew install ffmpeg")
        print("   - Linux: sudo apt-get install ffmpeg")
        print()
    
    if has_dependencies and has_ffmpeg:
        print("🎉 Setup Complete! You're ready to go!")
        print()
        print("Quick Start Options:")
        print()
        print("1. Start Web Interface:")
        print("   python app.py")
        print("   Then open: http://localhost:5000")
        print()
        print("2. Analyze Single File:")
        print("   python music_analyzer.py sample_tracks/your_song.mp3")
        print()
        print("3. Batch Process Directory:")
        print("   python batch_analyzer.py sample_tracks/")
        print()
        print("📖 Documentation:")
        print("   - README.md - Project overview")
        print("   - SETUP_GUIDE.md - Detailed installation guide")
        print("   - SAMPLE_ANALYSES.md - Example outputs")
    else:
        print("Complete the steps above, then run this script again!")
    
    print()
    print("="*70)


def main():
    """Main setup verification"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup cannot continue - Python version too old")
        sys.exit(1)
    
    # Check dependencies
    missing_deps = check_dependencies()
    has_dependencies = len(missing_deps) == 0
    
    # Check FFmpeg
    has_ffmpeg = check_ffmpeg()
    
    # Create directories
    create_directories()
    
    # Check files
    missing_files = check_files()
    
    if missing_files:
        print("\n⚠️  Warning: Some project files are missing!")
        print("   Make sure you have all the files from the project.")
    
    # Offer to install dependencies
    if missing_deps:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        response = input("\nInstall missing dependencies now? (y/n): ")
        if response.lower() == 'y':
            has_dependencies = install_dependencies()
    
    # Show next steps
    show_next_steps(has_dependencies, has_ffmpeg)
    
    # Final status
    print("\n" + "="*70)
    if has_dependencies and has_ffmpeg and not missing_files:
        print("✅ STATUS: READY TO USE")
        print("\nRun: python app.py")
    else:
        print("⚠️  STATUS: SETUP INCOMPLETE")
        print("Complete the steps above to finish setup")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)