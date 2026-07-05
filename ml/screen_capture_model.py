import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from ml.disaster_model import predict_disaster

model = tf.keras.models.load_model("ml/screen_image_detector.h5",compile=False)

async def predict_screen_capture(file):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((128,128))
    image_array = np.array(image)
    image_array = image_array/255.0
    Final_image = np.expand_dims(image_array,axis=0)
    prediction = model.predict(Final_image)[0][0]
    if prediction > 0.5:
        return{"Screen_captured_image"}
    else:
        print("length of image bytes:", len(image_bytes))
        return await predict_disaster(file)
        