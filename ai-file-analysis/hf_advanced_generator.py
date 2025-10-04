"""
Advanced AI-Powered File Description Generator
Uses state-of-the-art Hugging Face models for best results.

Recommended Models:
1. Moondream2 - Fast, lightweight vision model (BEST FOR YOUR CASE)
2. BLIP-2 - High quality vision-language model
3. Phi-3 Vision - Microsoft's vision-capable model
"""
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from PIL import Image
import torch
import PyPDF2


class AdvancedDescriptionGenerator:
    """Generate descriptions using advanced Hugging Face models."""
    
    def __init__(self, model_choice="moondream"):
        """
        Initialize with model choice.
        
        Options:
        - "moondream" (Recommended): Fast, lightweight, excellent quality
        - "blip2": High quality, slower, larger
        - "phi3-vision": Microsoft's vision model
        - "llava": Very detailed, slowest, largest
        """
        print(f"Loading {model_choice} model...")
        self.model_choice = model_choice
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        if model_choice == "moondream":
            self._load_moondream()
        elif model_choice == "blip2":
            self._load_blip2()
        elif model_choice == "phi3-vision":
            self._load_phi3_vision()
        elif model_choice == "llava":
            self._load_llava()
        else:
            raise ValueError(f"Unknown model: {model_choice}")
    
    def _load_moondream(self):
        """Load Moondream2 - Fast and excellent for technical images."""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            model_id = "vikhyatk/moondream2"
            revision = "2024-08-26"
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                trust_remote_code=True,
                revision=revision
            ).to(self.device)
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                revision=revision
            )
            
            print("✓ Moondream2 loaded successfully")
            self.generate_func = self._generate_moondream
            
        except Exception as e:
            print(f"Error loading Moondream: {e}")
            self.model = None
    
    def _load_blip2(self):
        """Load BLIP-2 - High quality vision-language model."""
        try:
            from transformers import Blip2Processor, Blip2ForConditionalGeneration
            
            self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
            self.model = Blip2ForConditionalGeneration.from_pretrained(
                "Salesforce/blip2-opt-2.7b",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            
            print("✓ BLIP-2 loaded successfully")
            self.generate_func = self._generate_blip2
            
        except Exception as e:
            print(f"Error loading BLIP-2: {e}")
            self.model = None
    
    def _load_phi3_vision(self):
        """Load Phi-3 Vision - Microsoft's vision model."""
        try:
            from transformers import AutoModelForCausalLM, AutoProcessor
            
            self.processor = AutoProcessor.from_pretrained(
                "microsoft/Phi-3-vision-128k-instruct",
                trust_remote_code=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                "microsoft/Phi-3-vision-128k-instruct",
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            
            print("✓ Phi-3 Vision loaded successfully")
            self.generate_func = self._generate_phi3_vision
            
        except Exception as e:
            print(f"Error loading Phi-3 Vision: {e}")
            self.model = None
    
    def _load_llava(self):
        """Load LLaVA - Very detailed descriptions."""
        try:
            from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
            
            self.processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
            self.model = LlavaNextForConditionalGeneration.from_pretrained(
                "llava-hf/llava-v1.6-mistral-7b-hf",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            
            print("✓ LLaVA loaded successfully")
            self.generate_func = self._generate_llava
            
        except Exception as e:
            print(f"Error loading LLaVA: {e}")
            self.model = None
    
    def _generate_moondream(self, image):
        """Generate description using Moondream2."""
        try:
            # Encode image
            enc_image = self.model.encode_image(image)
            
            # Generate description with specific prompt for technical content
            prompt = "Describe this image in detail, focusing on any text, diagrams, tables, or technical content visible."
            description = self.model.answer_question(enc_image, prompt, self.tokenizer)
            
            return description
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _generate_blip2(self, image):
        """Generate description using BLIP-2."""
        try:
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            
            generated_ids = self.model.generate(
                **inputs,
                max_length=150,
                num_beams=5
            )
            
            description = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True
            )[0].strip()
            
            return description
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _generate_phi3_vision(self, image):
        """Generate description using Phi-3 Vision."""
        try:
            messages = [
                {
                    "role": "user",
                    "content": "<|image_1|>\nDescribe this image in detail, focusing on any text, diagrams, tables, or technical content."
                }
            ]
            
            prompt = self.processor.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = self.processor(prompt, [image], return_tensors="pt").to(self.device)
            
            generate_ids = self.model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False
            )
            
            description = self.processor.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )[0]
            
            return description
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _generate_llava(self, image):
        """Generate description using LLaVA."""
        try:
            prompt = "USER: <image>\nDescribe this image in detail, focusing on any text, diagrams, tables, or technical content.\nASSISTANT:"
            
            inputs = self.processor(prompt, image, return_tensors="pt").to(self.device)
            
            output = self.model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False
            )
            
            description = self.processor.decode(output[0], skip_special_tokens=True)
            
            return description
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_image_description(self, image_path):
        """Generate description for an image."""
        if not self.model:
            return "AI model not available"
        
        try:
            image = Image.open(image_path).convert('RGB')
            description = self.generate_func(image)
            
            # Clean up description
            description = description.strip()
            if not description.endswith('.'):
                description += '.'
            
            return description
            
        except Exception as e:
            return f"Error processing image: {str(e)}"


def get_file_size_formatted(size_bytes):
    """Convert bytes to human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF."""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text.strip()
    except Exception as e:
        return f"PDF Error: {str(e)}"


def determine_risk_level(text_content, description):
    """Determine risk level based on content."""
    if not text_content and not description:
        return "Low"
    
    combined_text = (str(text_content) + " " + str(description)).lower()
    
    high_risk_keywords = ['password', 'secret', 'api key', 'token', 'credential', 
                          'ssn', 'credit card', 'confidential', 'private key', 'restricted']
    medium_risk_keywords = ['email', 'phone', 'address', 'personal', 'internal', 
                           'firewall', 'security', 'access', 'authentication']
    
    for keyword in high_risk_keywords:
        if keyword in combined_text:
            return "High"
    
    for keyword in medium_risk_keywords:
        if keyword in combined_text:
            return "Medium"
    
    return "Low"


def analyze_file_advanced(file_path, ai_generator):
    """Analyze a single file using advanced AI."""
    try:
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        file_size = os.path.getsize(file_path)
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"Processing: {file_name}")
        
        result = {
            'File Name': file_name,
            'File Type': file_ext,
            'File Size': get_file_size_formatted(file_size),
            'Risk Level': 'Low',
            'File Description': '',
            'Content Preview': '',
            'Key Findings': '',
            'Last Modified': last_modified
        }
        
        text_content = ""
        
        # Process based on file type
        if file_ext in ['.png', '.jpg', '.jpeg']:
            # Use AI for image description
            ai_description = ai_generator.generate_image_description(file_path)
            result['File Description'] = ai_description
            
            # Try OCR for additional context
            try:
                import pytesseract
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                img = Image.open(file_path)
                text_content = pytesseract.image_to_string(img).strip()
                
                if text_content:
                    preview = text_content[:150] + "..." if len(text_content) > 150 else text_content
                    result['Content Preview'] = f"[OCR Text] {preview}"
                else:
                    result['Content Preview'] = f"[AI Vision] {ai_description[:150]}"
                
                # Generate findings
                findings = []
                combined = (text_content + " " + ai_description).lower()
                
                if any(kw in combined for kw in ['password', 'secret', 'key', 'token', 'credential']):
                    findings.append("Contains potential credentials or sensitive authentication data")
                if any(kw in combined for kw in ['confidential', 'restricted', 'classified']):
                    findings.append("Marked as confidential or restricted access")
                if any(kw in combined for kw in ['email', 'phone', '@']):
                    findings.append("Contains personal contact information")
                if any(kw in combined for kw in ['firewall', 'rule', 'policy', 'access']):
                    findings.append("Contains security configuration or access control information")
                if any(kw in combined for kw in ['server', 'database', 'infrastructure']):
                    findings.append("Contains infrastructure or system architecture information")
                
                result['Key Findings'] = ". ".join(findings) + "." if findings else "AI-generated description available."
                
            except Exception as e:
                result['Content Preview'] = f"[AI Vision] {ai_description[:150]}"
                result['Key Findings'] = "AI-generated visual description available."
        
        elif file_ext == '.pdf':
            text_content = extract_text_from_pdf(file_path)
            
            if text_content and "PDF Error" not in text_content:
                result['File Description'] = "PDF document with text content."
                preview = text_content[:150] + "..." if len(text_content) > 150 else text_content
                result['Content Preview'] = f"[PDF] {preview}"
                result['Key Findings'] = "Text extracted from PDF."
            else:
                result['File Description'] = "PDF document, text extraction failed."
                result['Content Preview'] = f"[PDF: {file_name}] (No text extracted)"
                result['Key Findings'] = "PDF requires manual review."
        
        elif file_ext in ['.xlsx', '.xls']:
            result['File Description'] = "Excel spreadsheet, may contain data tables or reports."
            result['Content Preview'] = f"[Excel: {file_name}] Spreadsheet document."
            result['Key Findings'] = "Excel document detected."
        
        elif file_ext in ['.pptx', '.ppt']:
            result['File Description'] = "PowerPoint presentation with slides and content."
            result['Content Preview'] = f"[PowerPoint: {file_name}] Presentation document."
            result['Key Findings'] = "PowerPoint document detected."
        
        else:
            result['File Description'] = f"File of type {file_ext}"
            result['Content Preview'] = f"[File: {file_name}] Unknown file type."
            result['Key Findings'] = "File type not supported."
        
        # Determine risk level
        result['Risk Level'] = determine_risk_level(text_content, result['File Description'])
        
        return result
        
    except Exception as e:
        print(f"Error analyzing {file_path}: {str(e)}")
        return None


def main():
    """Main function."""
    print("="*80)
    print("ADVANCED AI-POWERED FILE ANALYSIS")
    print("="*80)
    print()
    
    # Choose model
    print("Available models:")
    print("1. moondream (Recommended) - Fast, lightweight, excellent quality")
    print("2. blip2 - High quality, slower, larger")
    print("3. phi3-vision - Microsoft's vision model")
    print("4. llava - Very detailed, slowest")
    print()
    
    model_choice = input("Choose model (1-4) or press Enter for default [1]: ").strip()
    
    model_map = {
        "1": "moondream",
        "2": "blip2",
        "3": "phi3-vision",
        "4": "llava",
        "": "moondream"
    }
    
    model = model_map.get(model_choice, "moondream")
    
    # Initialize AI generator
    ai_generator = AdvancedDescriptionGenerator(model)
    
    if not ai_generator.model:
        print("Failed to load model. Exiting.")
        return
    
    # Get files
    analysis_dir = Path("../Analysis Files/Files")
    if not analysis_dir.exists():
        print(f"Error: Directory {analysis_dir} not found!")
        return
    
    all_files = []
    for file_path in analysis_dir.iterdir():
        if file_path.is_file():
            file_name = file_path.name
            if not any(prefix in file_name for prefix in ['cleaned_', 'redacted_', 'precise_redacted_', 'preprocessed_']):
                all_files.append(file_path)
    
    print(f"\nFound {len(all_files)} files to process\n")
    
    # Process files
    results = []
    for idx, file_path in enumerate(sorted(all_files), start=0):
        result = analyze_file_advanced(str(file_path), ai_generator)
        if result:
            result['Index'] = idx
            results.append(result)
        print()
    
    # Save results
    if results:
        df = pd.DataFrame(results)
        df = df[['Index', 'File Name', 'File Type', 'File Size', 'Risk Level', 
                 'File Description', 'Content Preview', 'Key Findings', 'Last Modified']]
        
        output_file = f"ai_analysis_{model}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"✓ Results saved to {output_file}")
        
        try:
            excel_file = f"ai_analysis_{model}.xlsx"
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='AI Analysis')
            print(f"✓ Results saved to {excel_file}\n")
        except:
            pass
        
        print("="*150)
        print(f"AI ANALYSIS SUMMARY ({model.upper()})")
        print("="*150)
        print(df.to_string(index=False))
        print("="*150)


if __name__ == "__main__":
    main()
