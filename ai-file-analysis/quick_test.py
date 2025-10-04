"""Quick test script for individual files."""

import asyncio
import sys
from pathlib import Path

from src.services.simple_file_cleansing_service import SimpleFileCleansingService
from src.models.file_cleansing import CleansingConfiguration


async def quick_test_file(file_path):
    """Quick test of a single file."""
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"🧪 Testing file: {file_path.name}")
    print(f"📁 Location: {file_path.absolute()}")
    print(f"📊 Size: {file_path.stat().st_size:,} bytes")
    print(f"📄 Type: {file_path.suffix}")
    
    # Configure cleansing (aggressive settings)
    config = CleansingConfiguration(
        remove_all_macros=True,
        remove_location_data=True,
        remove_camera_info=True,
        remove_software_info=True,
        quarantine_suspicious_objects=True,
        neutralization_method="defang",
        extract_all_objects=False,
        preserve_safe_objects=True,
        create_backup=True
    )
    
    # Initialize service
    service = SimpleFileCleansingService()
    
    print(f"\n🚀 Starting cleansing process...")
    
    try:
        # Create output path
        output_path = file_path.parent / f"cleaned_{file_path.name}"
        
        # Process the file
        result = await service.cleanse_file(str(file_path), str(output_path), config)
        
        # Print results
        print(f"\n{'='*50}")
        print(f"📋 RESULTS")
        print(f"{'='*50}")
        
        if result.success:
            print(f"✅ Status: SUCCESS")
            print(f"⏱️  Processing time: {result.processing_time:.3f} seconds")
            print(f"📊 Size change: {result.original_size:,} → {result.cleaned_size:,} bytes")
            
            size_change = result.cleaned_size - result.original_size
            if size_change != 0:
                size_change_pct = (size_change / result.original_size * 100) if result.original_size > 0 else 0
                print(f"📈 Size difference: {size_change:+,} bytes ({size_change_pct:+.1f}%)")
            
            print(f"\n🔧 Actions taken:")
            if result.macros_removed > 0:
                print(f"   🚫 Removed {result.macros_removed} macro(s)")
            if result.objects_quarantined > 0:
                print(f"   🔒 Quarantined {result.objects_quarantined} object(s)")
            if result.urls_neutralized > 0:
                print(f"   🔗 Neutralized {result.urls_neutralized} URL(s)")
            if result.metadata_sanitized:
                print(f"   🧹 Sanitized metadata")
            
            if result.threats_detected:
                print(f"\n🛡️  Threats detected and removed:")
                for i, threat in enumerate(result.threats_detected, 1):
                    print(f"   {i}. {threat['type'].upper()}: {threat['description']}")
            else:
                print(f"\n✨ No threats detected - file appears clean!")
            
            if result.backup_location:
                print(f"\n💾 Backup saved: {Path(result.backup_location).name}")
            
            if result.quarantine_location:
                print(f"🔒 Quarantine location: {Path(result.quarantine_location).name}")
            
            print(f"\n📄 Cleaned file saved: {output_path.name}")
            
        else:
            print(f"❌ Status: FAILED")
            print(f"💥 Error: {result.error_message}")
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("🧪 Quick File Cleansing Test")
        print("Usage: python quick_test.py <file_path>")
        print("\nExample:")
        print("  python quick_test.py document.docx")
        print("  python quick_test.py image.jpg")
        print("  python quick_test.py presentation.pptx")
        return
    
    file_path = sys.argv[1]
    asyncio.run(quick_test_file(file_path))


if __name__ == "__main__":
    main()