import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model("ml/multi-Disaster_detector3.h5", compile=False)

classes = ["Earthquake","Flood","Landslide","Non_Disaster","Wildfire"]

async def predict_disaster(file):
    await file.seek(0)
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((128,128))
    image_array = np.array(image)
    image_array = image_array/255.0
    Final_image = np.expand_dims(image_array, axis=0)
    prediction = model.predict(Final_image)
    predicted_class = classes[np.argmax(prediction)]
    return predicted_class
