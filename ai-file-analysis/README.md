# AI-Powered File Analysis with Hugging Face

Automated file analysis system using Hugging Face vision models to generate intelligent descriptions for images, PDFs, and documents.

## Overview

This project analyzes files (screenshots, diagrams, PDFs, Office documents) and generates:
- AI-powered natural language descriptions
- Risk level assessment (Low/Medium/High)
- Content previews
- Security findings
- Comprehensive reports (CSV/Excel)

## Features

✅ **AI Vision Models** - Uses state-of-the-art Hugging Face models
✅ **Multiple Model Support** - Moondream2, BLIP-2, Phi-3 Vision, LLaVA
✅ **OCR Integration** - Extracts text from images
✅ **PDF Processing** - Analyzes PDF documents
✅ **Risk Assessment** - Automatic security risk classification
✅ **Excel Reports** - Professional formatted output

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_hf.txt
```

### 2. Run Analysis

```bash
python hf_advanced_generator.py
```

Choose your model:
- **Option 1: Moondream2** (Recommended) - Fast, lightweight, excellent for technical images
- **Option 2: BLIP-2** - High quality, detailed descriptions
- **Option 3: Phi-3 Vision** - Microsoft's vision model
- **Option 4: LLaVA** - Most detailed, best quality

### 3. View Results

Output files:
- `ai_analysis_[model].csv` - CSV format
- `ai_analysis_[model].xlsx` - Excel format

## Supported File Types

- **Images**: PNG, JPG, JPEG (with AI vision + OCR)
- **PDFs**: Text extraction and analysis
- **Office**: XLSX, PPTX, DOCX (metadata detection)

## Model Recommendations

### 🏆 Moondream2 (Recommended)
- **Best for**: Screenshots, diagrams, technical images
- **Size**: 1.6GB
- **Speed**: Fast (2-3 sec/image on CPU)
- **Quality**: Excellent

### Phi-3 Vision
- **Best for**: Microsoft ecosystem
- **Size**: 7GB
- **Speed**: Medium
- **Quality**: Very good

### BLIP-2
- **Best for**: High-quality descriptions
- **Size**: 5GB
- **Speed**: Medium
- **Quality**: Excellent

### LLaVA
- **Best for**: Maximum detail
- **Size**: 13GB
- **Speed**: Slow
- **Quality**: Best

## Example Output

### Input: Firewall Rules Screenshot

**AI Description:**
```
"This image shows a table of firewall rules with columns for rule name, 
direction, priority, action, and IP ranges. The rules include 
default-allow-internal, default-allow-ssh, default-allow-rdp, and 
default-allow-icmp, all set to ingress direction."
```

**Risk Level:** Medium
**Key Findings:** Contains security configuration or access control information

## Project Structure

```
ai-file-analysis/
├── hf_advanced_generator.py    # Main analysis script
├── requirements_hf.txt          # Dependencies
├── README.md                    # This file
├── MODEL_COMPARISON.md          # Detailed model comparison
├── WHICH_MODEL_TO_USE.md        # Model selection guide
├── HUGGINGFACE_GUIDE.md         # Complete usage guide
└── ../Analysis Files/           # Input files directory
    └── Files/
        ├── File_001.png
        ├── File_002.png
        └── ...
```

## Requirements

- Python 3.8+
- 8GB RAM minimum (16GB recommended)
- 3-15GB disk space (depending on model)
- Optional: NVIDIA GPU for faster processing

## Documentation

- **[MODEL_COMPARISON.md](MODEL_COMPARISON.md)** - Compare all available models
- **[WHICH_MODEL_TO_USE.md](WHICH_MODEL_TO_USE.md)** - Quick model selection guide
- **[HUGGINGFACE_GUIDE.md](HUGGINGFACE_GUIDE.md)** - Complete usage documentation
- **[RUN_AI_ANALYSIS.md](RUN_AI_ANALYSIS.md)** - Step-by-step instructions

## Output Format

| Column | Description |
|--------|-------------|
| Index | File number |
| File Name | Original filename |
| File Type | Extension (.png, .pdf, etc.) |
| File Size | Human-readable size |
| Risk Level | Low/Medium/High |
| File Description | AI-generated description |
| Content Preview | Text preview (OCR/extracted) |
| Key Findings | Security observations |
| Last Modified | Timestamp |

## GPU Acceleration (Optional)

For faster processing with NVIDIA GPU:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

Processing speed improvement: **5-10x faster**

## Troubleshooting

### Models not downloading
```bash
# Set cache directory
export HF_HOME=/path/to/cache
```

### Out of memory
- Use smaller model (Moondream2)
- Close other applications
- Process fewer files at once

### Slow processing
- Use GPU if available
- Choose faster model (Moondream2 or BLIP)
- Normal on CPU: 2-5 seconds per image

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines]

## Contact

[Your Contact Information]

---

**Ready to analyze your files with AI!** 🚀
