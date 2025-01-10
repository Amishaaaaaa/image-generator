from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
from workflow import generate_image  # Assuming you have a 'generate_image' function in 'workflow.py'
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Path where generated images will be stored
app.config['GENERATED_IMAGES'] = os.path.join(os.getcwd(), 'static/generated_images')

@app.route('/generate', methods=['POST'])
def generate():
    # Get data from the incoming request
    data = request.json
    
    # Generate image and get the file path (make sure `generate_image` returns the filename)
    image_path = generate_image(data)
    
    # Return the URL of the generated image
    return jsonify({"image_url": f"/static/generated_images/{image_path}"}), 200

@app.route('/static/generated_images/<path:filename>')
def get_image(filename):
    # Serve the generated image from the static folder
    return send_from_directory(app.config['GENERATED_IMAGES'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
