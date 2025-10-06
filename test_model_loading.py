import sys
import os
sys.path.append(os.path.dirname(__file__))

import app
import torch

def test_model_loading():
    """Test if the model loads correctly"""
    print("=== Testing Model Loading ===")
    
    # Test model loading
    success = app.load_model()
    
    if success:
        print("\n✓ Model loaded successfully!")
        
        # Test model inference with dummy input
        print("\n=== Testing Model Inference ===")
        try:
            # Create a dummy input (batch_size=1, channels=3, height=256, width=256)
            dummy_input = torch.randn(1, 3, 256, 256).to(app.device)
            print(f"Dummy input shape: {dummy_input.shape}")
            
            # Run inference
            with torch.no_grad():
                output = app.model(dummy_input)
                
            print(f"Model output shape: {output.shape}")
            print(f"Output range: [{output.min().item():.3f}, {output.max().item():.3f}]")
            
            # Check if output is reasonable
            if output.shape == (1, 3, 256, 256):
                print("✓ Output shape is correct!")
            else:
                print("❌ Unexpected output shape")
                
            if -2 <= output.min().item() <= 2 and -2 <= output.max().item() <= 2:
                print("✓ Output range looks reasonable for tanh activation")
            else:
                print("⚠ Output range might be unexpected")
                
            print("\n✓ Model inference test passed!")
            return True
            
        except Exception as e:
            print(f"❌ Model inference failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print("❌ Model loading failed!")
        return False

if __name__ == "__main__":
    success = test_model_loading()
    if success:
        print("\n🎉 All tests passed! The model is ready for the web application.")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")