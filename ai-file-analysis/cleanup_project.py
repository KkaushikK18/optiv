"""
Cleanup script to keep only essential files for HF analysis.
Removes all unnecessary code and keeps only what's needed.
"""
import os
import shutil
from pathlib import Path


# Files and folders to KEEP
KEEP_FILES = [
    # Main HF analysis script
    "hf_advanced_generator.py",
    
    # Documentation
    "MODEL_COMPARISON.md",
    "WHICH_MODEL_TO_USE.md",
    "HUGGINGFACE_GUIDE.md",
    "HUGGINGFACE_SUMMARY.md",
    "RUN_AI_ANALYSIS.md",
    
    # Requirements
    "requirements_hf.txt",
    
    # This cleanup script
    "cleanup_project.py",
    
    # README (if you want to create one)
    "README.md",
]

KEEP_FOLDERS = [
    # Your input data
    "../Analysis Files",
]

# Everything else will be removed
REMOVE_FOLDERS = [
    "src",
    "tests",
    "requirements",
    ".kiro",
]

REMOVE_FILES_PATTERNS = [
    "test_*.py",
    "analyze_all_files.py",
    "process_analysis_files.py",
    "hf_description_generator.py",
    "generate_html_report.py",
    "test_descriptions.py",
    "debug_*.py",
    "*.csv",
    "*.xlsx",
    "*.html",
    "Dockerfile",
    "docker-compose.yml",
    "*IMPLEMENTATION*.md",
    "*TASK_*.md",
    "HOW_TO_TEST.md",
    "DESCRIPTION_IMPROVEMENTS.md",
    "BEFORE_AFTER_COMPARISON.md",
    "ANALYSIS_FILES_GUIDE.md",
    "QUICK_START.md",
]


def should_keep_file(filename):
    """Check if file should be kept."""
    return filename in KEEP_FILES


def should_remove_file(filename):
    """Check if file matches removal patterns."""
    import fnmatch
    for pattern in REMOVE_FILES_PATTERNS:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def cleanup():
    """Perform cleanup."""
    print("="*80)
    print("CLEANUP: Keeping only essential HF analysis files")
    print("="*80)
    print()
    
    # Get current directory
    current_dir = Path(".")
    
    # Remove folders
    print("📁 Removing unnecessary folders...")
    for folder in REMOVE_FOLDERS:
        folder_path = current_dir / folder
        if folder_path.exists():
            print(f"  ❌ Removing: {folder}/")
            shutil.rmtree(folder_path)
    
    print()
    
    # Remove files
    print("📄 Removing unnecessary files...")
    for file_path in current_dir.glob("*"):
        if file_path.is_file():
            filename = file_path.name
            
            # Skip if should keep
            if should_keep_file(filename):
                print(f"  ✅ Keeping: {filename}")
                continue
            
            # Remove if matches pattern
            if should_remove_file(filename):
                print(f"  ❌ Removing: {filename}")
                file_path.unlink()
    
    print()
    print("="*80)
    print("✅ CLEANUP COMPLETE!")
    print("="*80)
    print()
    print("Files kept:")
    for file in KEEP_FILES:
        if (current_dir / file).exists():
            print(f"  ✅ {file}")
    
    print()
    print("Your project now contains only:")
    print("  1. hf_advanced_generator.py - Main HF analysis script")
    print("  2. Documentation (MD files)")
    print("  3. requirements_hf.txt - Dependencies")
    print("  4. ../Analysis Files/ - Your input data")
    print()
    print("Ready to combine with your GitHub code!")


if __name__ == "__main__":
    response = input("This will remove unnecessary files. Continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        cleanup()
    else:
        print("Cleanup cancelled.")
