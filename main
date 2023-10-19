from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import io

app = Flask(__name)

@app.route('/remove_background', methods=['POST'])
def remove_background():
    try:
        # Check if an image file was uploaded
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']

        # Check if the file is allowed
        if image_file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Read the uploaded image using PIL
        input_image = Image.open(image_file)
        
        # Removing the background
        output_image = remove(input_image)
        
        # Convert the output image to bytes
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        
        return jsonify({"result": "Background removed successfully", "image": output_buffer.getvalue().decode('latin1')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
