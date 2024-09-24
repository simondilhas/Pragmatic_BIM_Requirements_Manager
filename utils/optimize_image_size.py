import os
import argparse
from PIL import Image
import io

def optimize_image(input_path, output_path, max_size_kb=500, quality=85):
    with open(input_path, 'rb') as f:
        image_content = f.read()
    
    img = Image.open(io.BytesIO(image_content))
    
    # Convert to RGB if image is in CMYK mode
    if img.mode == 'CMYK':
        img = img.convert('RGB')
    
    # Calculate current size in KB
    current_size = len(image_content) / 1024
    
    # If the image is already smaller than max_size_kb, save it as is
    if current_size <= max_size_kb:
        img.save(output_path, optimize=True)
        return
    
    # Start with the original size
    width, height = img.size
    
    while current_size > max_size_kb:
        # Reduce dimensions by 10%
        width = int(width * 0.9)
        height = int(height * 0.9)
        
        # Resize and save to a bytes buffer
        img_resized = img.resize((width, height), Image.LANCZOS)
        buffer = io.BytesIO()
        img_resized.save(buffer, format='JPEG', quality=quality, optimize=True)
        
        # Update current size
        current_size = len(buffer.getvalue()) / 1024
        
        # Reduce quality if size is still too large
        if current_size > max_size_kb:
            quality -= 5
        
        # Break if quality becomes too low
        if quality < 20:
            break
    
    # Save the optimized image
    img_resized.save(output_path, format='JPEG', quality=quality, optimize=True)

def main():
    parser = argparse.ArgumentParser(description="Optimize images in a directory")
    parser.add_argument("input_dir", help="Input directory containing images")
    parser.add_argument("output_dir", help="Output directory for optimized images")
    parser.add_argument("--max-size", type=int, default=500, help="Maximum file size in KB (default: 500)")
    parser.add_argument("--quality", type=int, default=85, help="Initial JPEG quality (default: 85)")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    for filename in os.listdir(args.input_dir):
        input_path = os.path.join(args.input_dir, filename)
        
        # Check if it's a file and has a supported extension
        if os.path.isfile(input_path) and os.path.splitext(filename)[1].lower() in supported_formats:
            output_path = os.path.join(args.output_dir, filename)
            
            try:
                optimize_image(input_path, output_path, args.max_size, args.quality)
                print(f"Optimized: {filename}")
            except Exception as e:
                print(f"Error optimizing {filename}: {e}")

if __name__ == "__main__":
    main()