# 🎨 Sketch2Face Web Application - Usage Guide

## 🚀 Quick Start

### Option 1: One-Click Startup (Easiest)
1. Double-click `start_app.bat` in your file explorer
2. Wait for the application to start (you'll see the Flask server running)
3. Open your web browser and go to: **http://localhost:5000**

### Option 2: Manual Startup
```cmd
cd D:\sketch2face_webapp
venv\Scripts\activate
python app.py
```

## 🌐 Using the Web Interface

### 1. **Upload Your Sketch**
- **Drag & Drop**: Simply drag your sketch image onto the upload area
- **Browse**: Click the "Browse Files" button to select from your computer
- **Supported formats**: PNG, JPEG, GIF, BMP
- **Size limit**: 16MB maximum

### 2. **Generate Face**
- After uploading, click the **"Generate Face"** button
- The AI will process your sketch (takes a few seconds)
- You'll see a loading spinner during processing

### 3. **View Results**
- Compare your original sketch with the generated face side-by-side
- The generated image appears on the right
- Both images are automatically resized for optimal viewing

### 4. **Download Result**
- Click the **"Download"** button to save the generated face to your computer
- Images are saved in high quality

## ✨ What Makes This Special

### Your Trained Model
- **Model**: U-Net Generator with 54,414,531 parameters
- **Training**: 100 epochs with best loss of 12.931054
- **Architecture**: 8-layer encoder-decoder with skip connections
- **Input/Output**: 256x256 RGB images

### Technical Features
- **GPU Support**: Automatically uses GPU if available, falls back to CPU
- **Real-time Processing**: Fast inference with optimized preprocessing
- **Memory Efficient**: Proper tensor management and cleanup
- **Error Handling**: Graceful handling of various image formats and sizes

## 📸 Tips for Best Results

### Input Sketches
- **Clear lines**: Bold, clear outlines work best
- **Face focus**: Center the face in the image
- **Contrast**: Good contrast between lines and background
- **Resolution**: Any resolution (will be resized to 256x256)

### Example Sketches to Try
- Simple line drawings of faces
- Pencil sketches with clear features
- Digital drawings with defined features
- Hand-drawn portraits

## 🛠️ Technical Details

### Model Architecture
```
U-Net Generator:
├── Encoder (8 layers): 3→64→128→256→512→512→512→512→512
├── Decoder (8 layers): 512→512→512→512→256→128→64→3
└── Skip connections between encoder/decoder layers
```

### Processing Pipeline
1. **Input**: Upload sketch image
2. **Preprocessing**: Resize to 256×256, normalize to [-1,1]
3. **Inference**: Pass through U-Net generator
4. **Postprocessing**: Denormalize, convert to displayable format
5. **Output**: Generated face image

### Server Endpoints
- `GET /` - Main web interface
- `POST /upload` - Process sketch and generate face
- `GET /download/<filename>` - Download generated image
- `GET /health` - Check server status

## 🔧 Troubleshooting

### Common Issues

**🚫 "Model loading failed"**
- Ensure the model file exists: `D:\sketch2face\dynamic_checkpoints\dynamic_best_model.pt`
- Check that you have sufficient RAM (model needs ~220MB)

**🚫 "Port 5000 already in use"**
- Close other applications using port 5000
- Or change the port in `app.py`: `app.run(host='0.0.0.0', port=5001)`

**🚫 "Out of memory"**
- Close other applications to free up RAM
- The model runs on CPU by default (no GPU required)

**🚫 "Upload failed"**
- Check file size (must be < 16MB)
- Ensure file is a valid image format
- Try a different image

### Performance Tips
- **For faster processing**: Ensure you have available RAM
- **For GPU acceleration**: Install CUDA-compatible PyTorch if you have an NVIDIA GPU
- **For multiple users**: Consider using a production WSGI server instead of Flask's development server

## 📱 Access from Other Devices

The server runs on all network interfaces, so you can access it from:
- **Same computer**: http://localhost:5000
- **Other devices on network**: http://[YOUR_IP]:5000
  - Check the Flask startup output for your IP address
  - Example: `http://10.202.125.55:5000`

## 🎯 Next Steps

### Deployment Options
1. **Local Network**: Already configured for local network access
2. **Cloud Deployment**: Can be deployed to services like Heroku, AWS, or Google Cloud
3. **Docker**: Can be containerized for easier deployment

### Customization
- **UI Styling**: Modify `static/style.css`
- **Processing**: Adjust preprocessing in `app.py`
- **Model**: Swap in different trained models

---

## 🎉 Enjoy Your Sketch2Face Web Application!

Your AI model is now live and ready to transform sketches into realistic faces. Share the URL with others on your network to let them try it too!

**Need help?** Check the console output for detailed error messages and status updates.