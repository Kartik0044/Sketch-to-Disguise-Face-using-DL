from PIL import Image, ImageDraw
import numpy as np

def create_test_sketch():
    """Create a simple sketch-like test image"""
    # Create a white background
    img = Image.new('RGB', (256, 256), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple face outline (black lines on white background)
    # Face oval
    draw.ellipse([50, 40, 206, 200], outline='black', width=3)
    
    # Eyes
    draw.ellipse([70, 90, 90, 110], outline='black', width=2)  # Left eye
    draw.ellipse([166, 90, 186, 110], outline='black', width=2)  # Right eye
    
    # Nose
    draw.line([128, 110, 128, 140], fill='black', width=2)
    draw.line([118, 140, 128, 140], fill='black', width=2)
    draw.line([128, 140, 138, 140], fill='black', width=2)
    
    # Mouth
    draw.arc([100, 150, 156, 180], start=0, end=180, fill='black', width=3)
    
    # Hair (some simple lines)
    for i in range(10):
        x_start = 60 + i * 15
        draw.line([x_start, 40, x_start + 5, 20], fill='black', width=2)
    
    # Save the test image
    img.save('test_sketch.png')
    print("Test sketch saved as 'test_sketch.png'")
    return img

if __name__ == "__main__":
    create_test_sketch()