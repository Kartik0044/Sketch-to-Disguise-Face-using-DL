import torch
import sys

def inspect_model():
    """Inspect the structure of the trained model checkpoint"""
    try:
        model_path = r"D:\sketch2face\dynamic_checkpoints\dynamic_best_model.pt"
        print(f"Loading model from: {model_path}")
        
        # Load the checkpoint (trust the source since it's our own model)
        checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
        
        print("\n=== CHECKPOINT STRUCTURE ===")
        print(f"Checkpoint type: {type(checkpoint)}")
        
        if isinstance(checkpoint, dict):
            print("\nCheckpoint keys:")
            for key in checkpoint.keys():
                print(f"  - {key}: {type(checkpoint[key])}")
                if isinstance(checkpoint[key], dict):
                    print(f"    Keys in {key}: {list(checkpoint[key].keys())[:5]}...")  # Show first 5 keys
        
        # Try to get the model state dict
        if isinstance(checkpoint, dict):
            if 'generator_state_dict' in checkpoint:
                state_dict = checkpoint['generator_state_dict']
                print("\n=== GENERATOR STATE DICT ===")
            elif 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
                print("\n=== MODEL STATE DICT ===")
            elif 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
                print("\n=== MODEL STATE DICT (from 'state_dict' key) ===")
            else:
                # Checkpoint might be the state dict itself
                state_dict = checkpoint
                print("\n=== MODEL STATE DICT (checkpoint is state dict) ===")
        else:
            print("Checkpoint is not a dictionary, might be a model directly")
            return
        
        # Analyze the model layers
        print("\nModel layers:")
        layer_info = {}
        for name, param in state_dict.items():
            layer_name = name.split('.')[0]  # Get the base layer name
            if layer_name not in layer_info:
                layer_info[layer_name] = []
            layer_info[layer_name].append({
                'name': name,
                'shape': param.shape if hasattr(param, 'shape') else 'N/A',
                'dtype': param.dtype if hasattr(param, 'dtype') else 'N/A'
            })
        
        for layer, params in layer_info.items():
            print(f"\n  {layer}:")
            for param in params[:3]:  # Show first 3 parameters per layer
                print(f"    - {param['name']}: {param['shape']} ({param['dtype']})")
            if len(params) > 3:
                print(f"    ... and {len(params) - 3} more parameters")
        
        # Try to infer model architecture
        print("\n=== MODEL ARCHITECTURE ANALYSIS ===")
        total_params = sum(p.numel() for p in state_dict.values() if hasattr(p, 'numel'))
        print(f"Total parameters: {total_params:,}")
        
        # Look for common GAN/CNN patterns
        has_generator = any('generator' in key.lower() or 'gen' in key.lower() for key in state_dict.keys())
        has_discriminator = any('discriminator' in key.lower() or 'disc' in key.lower() for key in state_dict.keys())
        has_encoder = any('encoder' in key.lower() or 'enc' in key.lower() for key in state_dict.keys())
        has_decoder = any('decoder' in key.lower() or 'dec' in key.lower() for key in state_dict.keys())
        
        print(f"Has Generator: {has_generator}")
        print(f"Has Discriminator: {has_discriminator}")
        print(f"Has Encoder: {has_encoder}")
        print(f"Has Decoder: {has_decoder}")
        
        # Look for input/output dimensions
        first_layer = None
        last_layer = None
        for name, param in state_dict.items():
            if 'weight' in name and len(param.shape) >= 2:
                if first_layer is None:
                    first_layer = (name, param.shape)
                last_layer = (name, param.shape)
        
        if first_layer:
            print(f"\nFirst layer: {first_layer[0]} - Shape: {first_layer[1]}")
        if last_layer:
            print(f"Last layer: {last_layer[0]} - Shape: {last_layer[1]}")
        
        print("\n=== RECOMMENDATIONS ===")
        if has_generator:
            print("✓ This appears to be a GAN model with a generator")
            print("  Suggestion: Use only the generator for inference")
        else:
            print("✓ This appears to be a direct mapping model")
            print("  Suggestion: Use the entire model for inference")
        
    except Exception as e:
        print(f"Error inspecting model: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect_model()