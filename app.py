from flask import Flask, request, render_template, jsonify, send_from_directory
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os
import io
import base64
import numpy as np
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variable to store the loaded model
model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# U-Net Generator Architecture - Matching Training Script
class UNetGenerator(nn.Module):
    """U-Net Generator with skip connections - Exact match with training script"""
    
    def __init__(self, input_nc=3, output_nc=3, ngf=64):
        super(UNetGenerator, self).__init__()
        
        # Encoder (Contracting path) - matching training script exactly
        self.enc1 = self.conv_block(input_nc, ngf, normalize=False, dropout=False)
        self.enc2 = self.conv_block(ngf, ngf * 2, normalize=True, dropout=False)
        self.enc3 = self.conv_block(ngf * 2, ngf * 4, normalize=True, dropout=False)
        self.enc4 = self.conv_block(ngf * 4, ngf * 8, normalize=True, dropout=False)
        self.enc5 = self.conv_block(ngf * 8, ngf * 8, normalize=True, dropout=False)
        self.enc6 = self.conv_block(ngf * 8, ngf * 8, normalize=True, dropout=False)
        self.enc7 = self.conv_block(ngf * 8, ngf * 8, normalize=True, dropout=False)
        self.enc8 = self.conv_block(ngf * 8, ngf * 8, normalize=False, dropout=False)
        
        # Decoder (Expanding path) - matching training script exactly
        self.dec1 = self.deconv_block(ngf * 8, ngf * 8, normalize=True, dropout=True)
        self.dec2 = self.deconv_block(ngf * 16, ngf * 8, normalize=True, dropout=True)
        self.dec3 = self.deconv_block(ngf * 16, ngf * 8, normalize=True, dropout=True)
        self.dec4 = self.deconv_block(ngf * 16, ngf * 8, normalize=True, dropout=False)
        self.dec5 = self.deconv_block(ngf * 16, ngf * 4, normalize=True, dropout=False)
        self.dec6 = self.deconv_block(ngf * 8, ngf * 2, normalize=True, dropout=False)
        self.dec7 = self.deconv_block(ngf * 4, ngf, normalize=True, dropout=False)
        self.dec8 = self.final_deconv_block(ngf * 2, output_nc)
    
    def conv_block(self, in_c, out_c, normalize=True, dropout=False):
        layers = [nn.Conv2d(in_c, out_c, 4, 2, 1, bias=False if normalize else True)]
        if normalize:
            layers.append(nn.BatchNorm2d(out_c))
        layers.append(nn.LeakyReLU(0.2, True))
        if dropout:
            layers.append(nn.Dropout(0.5))
        return nn.Sequential(*layers)
    
    def deconv_block(self, in_c, out_c, normalize=True, dropout=False):
        layers = [nn.ConvTranspose2d(in_c, out_c, 4, 2, 1, bias=False if normalize else True)]
        if normalize:
            layers.append(nn.BatchNorm2d(out_c))
        layers.append(nn.ReLU(True))
        if dropout:
            layers.append(nn.Dropout(0.5))
        return nn.Sequential(*layers)
    
    def final_deconv_block(self, in_c, out_c):
        return nn.Sequential(
            nn.ConvTranspose2d(in_c, out_c, 4, 2, 1),
            nn.Tanh()
        )
    
    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(e1)
        e3 = self.enc3(e2)
        e4 = self.enc4(e3)
        e5 = self.enc5(e4)
        e6 = self.enc6(e5)
        e7 = self.enc7(e6)
        e8 = self.enc8(e7)
        
        # Decoder with skip connections
        d1 = self.dec1(e8)
        d2 = self.dec2(torch.cat([d1, e7], 1))
        d3 = self.dec3(torch.cat([d2, e6], 1))
        d4 = self.dec4(torch.cat([d3, e5], 1))
        d5 = self.dec5(torch.cat([d4, e4], 1))
        d6 = self.dec6(torch.cat([d5, e3], 1))
        d7 = self.dec7(torch.cat([d6, e2], 1))
        d8 = self.dec8(torch.cat([d7, e1], 1))
        
        return d8

def load_model():
    """Load the trained model from the checkpoint"""
    global model
    try:
        model_path = r"D:\sketch2face\dynamic_checkpoints\dynamic_best_model.pt"
        
        # Initialize U-Net generator architecture
        model = UNetGenerator(input_nc=3, output_nc=3, ngf=64)
        
        # Load the checkpoint (trust our own model)
        checkpoint = torch.load(model_path, map_location=device, weights_only=False)
        
        # Load generator state dict
        if 'generator_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['generator_state_dict'])
            print("Loaded generator state dict")
        elif 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
            print("Loaded model state dict")
        else:
            model.load_state_dict(checkpoint)
            print("Loaded checkpoint as state dict")
            
        model.to(device)
        model.eval()
        
        # Print model info
        total_params = sum(p.numel() for p in model.parameters())
        print(f"Model loaded successfully from {model_path}")
        print(f"Total parameters: {total_params:,}")
        print(f"Device: {device}")
        
        # Print detailed checkpoint info if available
        if isinstance(checkpoint, dict):
            if 'epoch' in checkpoint:
                print(f"✅ Model trained for {checkpoint['epoch']} epochs")
            if 'best_loss' in checkpoint:
                print(f"📊 Best loss achieved: {checkpoint['best_loss']:.6f}")
            if 'datasets_used' in checkpoint:
                print(f"📁 Datasets used: {checkpoint['datasets_used']}")
            if 'total_samples' in checkpoint:
                print(f"🎯 Total training samples: {checkpoint['total_samples']:,}")
        
        return True
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def preprocess_image(image):
    """Preprocess the input image for the model"""
    # Define transforms - typical for GAN training (256x256, normalized to [-1, 1])
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Resize to model input size
        transforms.ToTensor(),          # Convert to tensor [0, 1]
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize to [-1, 1]
    ])
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Apply transforms
    tensor_image = transform(image).unsqueeze(0)  # Add batch dimension
    return tensor_image.to(device)

def postprocess_output(output_tensor):
    """Convert model output back to PIL Image"""
    # Move to CPU and detach from computation graph
    output_tensor = output_tensor.detach().cpu()
    
    # Denormalize from [-1, 1] to [0, 1]
    output_tensor = (output_tensor + 1) / 2.0
    output_tensor = torch.clamp(output_tensor, 0, 1)
    
    # Convert to PIL Image
    output_np = output_tensor.squeeze(0).numpy()  # Remove batch dimension
    output_np = (output_np.transpose(1, 2, 0) * 255).astype(np.uint8)  # CHW -> HWC, scale to [0, 255]
    return Image.fromarray(output_np)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and model inference"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            
            # Save uploaded file
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            
            # Load and preprocess image
            image = Image.open(upload_path)
            input_tensor = preprocess_image(image)
            
            # Run inference
            with torch.no_grad():
                output_tensor = model(input_tensor)
            
            # Postprocess output
            output_image = postprocess_output(output_tensor)
            
            # Save output image
            output_filename = 'output_' + filename
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            output_image.save(output_path)
            
            # Convert output image to base64 for display
            img_buffer = io.BytesIO()
            output_image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode()
            
            return jsonify({
                'success': True,
                'output_image': f'data:image/png;base64,{img_base64}',
                'output_filename': output_filename
            })
            
        except Exception as e:
            return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated image"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'device': str(device)
    })

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    # Load the model
    if load_model():
        print("Starting Flask application...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Failed to load model. Please check the model path and try again.")