import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model


model = None


def get_model():
    global model

    if model is None:
        model = load_model(
            "ml/multi-Disaster_detector3.h5",
            compile=False
        )

    return model


classes = ["Earthquake","Flood","Landslide","Non_Disaster","Wildfire"]


# async def predict_disaster(file):

#     model = get_model()

#     await file.seek(0)

#     image_bytes = await file.read()

#     image = Image.open(
#         io.BytesIO(image_bytes)
#     ).convert("RGB")

#     image = image.resize((128,128))

#     image_array = np.array(image)
#     image_array = image_array / 255.0

#     Final_image = np.expand_dims(image_array, axis=0)

#     prediction = model.predict(Final_image)

#     predicted_class = classes[np.argmax(prediction)]

#     return predicted_class



import time

async def predict_disaster(file):
    model = get_model()
    print("file type:", type(file), flush=True)
    total_start = time.perf_counter()

    # File
    t1 = time.perf_counter()
    await file.seek(0)
    t2 = time.perf_counter()

    image_bytes = await file.read()
    t3 = time.perf_counter()

    # Image preprocessing
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((128, 128))

    image_array = np.array(image)
    image_array = image_array / 255.0
    final_image = np.expand_dims(image_array, axis=0)

    t4 = time.perf_counter()

    # CNN
    prediction = model.predict(final_image, verbose=0)

    t5 = time.perf_counter()

    predicted_class = classes[np.argmax(prediction)]

    print("seek:", t2 - t1)
    print("read:", t3 - t2)
    print("preprocessing:", t4 - t3)
    print("inference:", t5 - t4)
    print("TOTAL:", t5 - total_start, flush=True)

    return predicted_class

