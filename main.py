from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import io
import shutil
import os

app = FastAPI()

# Directory to save temporary image files
output_dir = 'output_images/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

@app.post("/remove_bg/")
async def remove_background(file: UploadFile):
    # Save the uploaded image temporarily
    image_path = os.path.join(output_dir, file.filename)
    with open(image_path, "wb") as img_file:
        shutil.copyfileobj(file.file, img_file)

    # Remove the background
    input_image = Image.open(image_path)
    output_image = remove(input_image)

    # Save the output image temporarily
    output_path = os.path.join(output_dir, f'removed_{file.filename}')
    output_image.save(output_path, "PNG")

    return FileResponse(output_path, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
