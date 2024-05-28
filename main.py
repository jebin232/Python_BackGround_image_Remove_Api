from flask import Flask, request, jsonify, send_file, render_template
from rembg import remove
from PIL import Image
import PIL
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remove_background/', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({"detail": "No image provided"}), 400

    file = request.files['image']
    image = Image.open(file.stream)
    output = remove(image)
    
    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return send_file(io.BytesIO(img_byte_arr), mimetype='image/png')

@app.route('/change_background/', methods=['POST'])
def change_background():
    if 'image' not in request.files or 'background' not in request.files:
        return jsonify({"detail": "Image or background not provided"}), 400

    image_file = request.files['image']
    background_file = request.files['background']

    image = Image.open(image_file.stream)
    background = Image.open(background_file.stream).convert("RGBA")

    output = remove(image)
    background = background.resize(output.size, PIL.Image.Resampling.LANCZOS)

    combined = Image.alpha_composite(background, output)
    
    img_byte_arr = io.BytesIO()
    combined.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return send_file(io.BytesIO(img_byte_arr), mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
