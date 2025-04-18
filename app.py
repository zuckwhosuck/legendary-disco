from flask import Flask, request, render_template, jsonify  
import os  
from werkzeug.utils import secure_filename  
from PIL import Image  
import base64  
import logging
logging.basicConfig(level=logging.DEBUG)
  
from models.model_loader import load_model, predict_image  
  
app = Flask(__name__)  
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload  
app.config['UPLOAD_FOLDER'] = 'uploads'  
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}  
app.secret_key = os.urandom(24)  
  
# Create upload folder if it doesn't exist  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  
  
# Lazy load model: only load once on first use  
model = None  
def get_model():  
    global model  
    if model is None:  
        model = load_model()  
    return model  
  
def allowed_file(filename):  
    """Check if the file extension is allowed."""  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']  
  
@app.route('/')  
def index():  
    """Render the main HTML page."""  
    return render_template('index.html')  
  
@app.route('/about')  
def about():  
    return render_template('about.html')  
  
@app.route('/api/detect', methods=['POST'])  
def detect_deepfake():  
    """Handle deepfake detection API request."""  
    if 'file' not in request.files:  
        return jsonify({'error': 'No file part'}), 400  
  
    file = request.files['file']  
  
    if file.filename == '':  
        return jsonify({'error': 'No selected file'}), 400  
  
    if file and allowed_file(file.filename):  
        try:  
            filename = secure_filename(file.filename)  
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
            file.save(file_path)  
  
            # Open and process the image  
            image = Image.open(file_path).convert('RGB')  
            model_instance = get_model()  
            prediction_result = predict_image(model_instance, image)  
  
            if "error" in prediction_result:  
                return jsonify({'error': prediction_result["error"]}), 500  
  
            # Encode the image to base64 for display  
            with open(file_path, "rb") as img_file:  
                img_str = base64.b64encode(img_file.read()).decode('utf-8')  
  
            return jsonify({  
                'success': True,  
                'prediction': prediction_result['prediction'],  
                'confidence': prediction_result['confidence'],  
                'all_scores': prediction_result['all_scores'],  
                'image': f'data:image/jpeg;base64,{img_str}'  
            })  
  
        except Exception as e:  
            return jsonify({'error': str(e)}), 500  
  
    return jsonify({'error': 'File type not allowed'}), 400  
  
if __name__ == '__main__':  
    port = int(os.environ.get("PORT", 10000))  
    app.run(debug=True, host='0.0.0.0', port=port)
