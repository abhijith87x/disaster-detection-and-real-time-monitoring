import numpy as np
import io
from PIL import Image
import tensorflow as tf

from disaster_prediction_model import predict_disaster


model = None


def get_screen_model():
    global model

    if model is None:
        model = tf.keras.models.load_model(
            "ml/screen_image_detector.h5",
            compile=False
        )

    return model


async def predict_screen_capture(file):

    model = get_screen_model()

    await file.seek(0)

    image_bytes = await file.read()

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    image = image.resize((128, 128))

    image_array = np.array(image)
    image_array = image_array / 255.0

    final_image = np.expand_dims(
        image_array,
        axis=0
    )

    prediction = model.predict(final_image)[0][0]

    if prediction > 0.5:
        return "Screen_captured_image"

    else:

        return await predict_disaster(file)