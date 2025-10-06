# Sketch2Face Web Application

This web application allows users to upload sketch images and convert them to realistic faces using a trained deep learning model.

## Features

- **Easy Upload**: Drag & drop or click to browse sketch images
- **Real-time Processing**: AI-powered sketch-to-face conversion
- **Download Results**: Save generated face images
- **Responsive Design**: Works on desktop and mobile devices
- **Multiple Formats**: Supports PNG, JPEG, GIF, and BMP images

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Your trained model file: `D:\sketch2face\dynamic_checkpoints\dynamic_best_model.pt`

### Installation

1. **Navigate to the project directory:**
   ```cmd
   cd D:\sketch2face_webapp
   ```

2. **Create a virtual environment (recommended):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **For GPU support (if you have CUDA available):**
   ```cmd
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### Running the Application

1. **Start the Flask server:**
   ```cmd
   python app.py
   ```

2. **Open your web browser and go to:**
   ```
   http://localhost:5000
   ```

## Usage

1. **Upload a Sketch**: Click the upload area or drag & drop a sketch image
2. **Generate Face**: Click the "Generate Face" button to process your sketch
3. **View Results**: See the original sketch and generated face side by side
4. **Download**: Save the generated face image to your device

## Project Structure

```
sketch2face_webapp/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface template
├── static/
│   └── style.css         # CSS styling
├── uploads/              # Uploaded images (auto-created)
├── outputs/              # Generated images (auto-created)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Important Notes

⚠️ **Model Architecture**: The current `app.py` contains a placeholder model architecture. You'll need to modify the `Sketch2FaceModel` class to match your actual trained model architecture.

🔧 **Model Loading**: If your model checkpoint has a different structure, you may need to adjust the `load_model()` function.

🖼️ **Image Processing**: The preprocessing and postprocessing functions may need adjustment based on how your model was trained.

## Customization

### Model Architecture
Edit the `Sketch2FaceModel` class in `app.py` to match your trained model.

### Image Preprocessing
Modify the `preprocess_image()` function to match your training preprocessing steps.

### UI Styling
Update `static/style.css` to customize the appearance.

## Troubleshooting

**Model Loading Issues:**
- Ensure the model path is correct: `D:\sketch2face\dynamic_checkpoints\dynamic_best_model.pt`
- Check that the model architecture matches your trained model

**Memory Issues:**
- The app automatically uses GPU if available, CPU otherwise
- For large models, ensure sufficient RAM/VRAM

**Port Conflicts:**
- If port 5000 is busy, change the port in `app.py`: `app.run(host='0.0.0.0', port=YOUR_PORT)`

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload and process image
- `GET /download/<filename>` - Download generated image
- `GET /health` - Check application health

## License

This project is for educational and research purposes.