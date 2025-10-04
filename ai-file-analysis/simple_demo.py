"""Simple demonstration of file cleansing."""

import asyncio
import tempfile
import zipfile
from pathlib import Path

from src.services.simple_file_cleansing_service import SimpleFileCleansingService
from src.models.file_cleansing import CleansingConfiguration


def create_test_docx_with_threats(file_path):
    """Create a DOCX file with various threats."""
    
    with zipfile.ZipFile(file_path, 'w') as zf:
        # Content Types
        zf.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    <Override PartName="/word/vbaProject.bin" ContentType="application/vnd.ms-office.vbaProject"/>
</Types>''')
        
        # Main relationships
        zf.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''')
        
        # Document with malicious URLs
        zf.writestr('word/document.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p><w:r><w:t>Business Proposal Document</w:t></w:r></w:p>
        <w:p><w:r><w:t>Please visit: http://malicious-site.com/download</w:t></w:r></w:p>
        <w:p><w:r><w:t>Or check: https://phishing-site.net/login</w:t></w:r></w:p>
        <w:p><w:r><w:t>FTP access: ftp://insecure-server.com/files</w:t></w:r></w:p>
        <w:p><w:r><w:t>Safe site: https://www.google.com</w:t></w:r></w:p>
    </w:body>
</w:document>''')
        
        # VBA project (macro)
        zf.writestr('word/vbaProject.bin', b'VBA macro with Shell("cmd.exe /c malicious_command")')
        
        # Document relationships
        zf.writestr('word/_rels/document.xml.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/vbaProject" Target="vbaProject.bin"/>
</Relationships>''')


async def simple_demo():
    """Run a simple demonstration."""
    
    print("🧪 SIMPLE FILE CLEANSING DEMO")
    print("=" * 40)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test file
        test_file = temp_path / "test_document.docx"
        create_test_docx_with_threats(test_file)
        
        original_size = test_file.stat().st_size
        print(f"📄 Created test file: {test_file.name}")
        print(f"📊 Original size: {original_size:,} bytes")
        
        # Configure cleansing
        config = CleansingConfiguration(
            remove_all_macros=True,
            quarantine_suspicious_objects=True,
            neutralization_method="defang",
            create_backup=True
        )
        
        print(f"\n⚙️  Configuration:")
        print(f"   🚫 Remove macros: {config.remove_all_macros}")
        print(f"   🔒 Quarantine objects: {config.quarantine_suspicious_objects}")
        print(f"   🔗 Neutralize URLs: {config.neutralization_method}")
        
        # Process file
        service = SimpleFileCleansingService()
        
        print(f"\n🚀 Processing file...")
        result = await service.cleanse_file(str(test_file), None, config)
        
        # Show results
        print(f"\n📋 RESULTS:")
        print(f"✅ Success: {result.success}")
        print(f"⏱️  Time: {result.processing_time:.3f} seconds")
        print(f"📊 Size: {original_size:,} → {result.cleaned_size:,} bytes")
        
        if result.threats_detected:
            print(f"\n🛡️  Threats found and removed:")
            for i, threat in enumerate(result.threats_detected, 1):
                print(f"   {i}. {threat['type'].upper()}: {threat['description']}")
        
        print(f"\n🔧 Actions taken:")
        if result.macros_removed > 0:
            print(f"   🚫 Removed {result.macros_removed} macro(s)")
        if result.objects_quarantined > 0:
            print(f"   🔒 Quarantined {result.objects_quarantined} object(s)")
        if result.urls_neutralized > 0:
            print(f"   🔗 Neutralized {result.urls_neutralized} URL(s)")
        
        if result.backup_location:
            print(f"\n💾 Backup: {Path(result.backup_location).name}")
        
        print(f"\n✨ File successfully cleaned!")


if __name__ == "__main__":
    asyncio.run(simple_demo())