import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model("ml/multi-Disaster_detector3.keras", compile=False)
classes = ["Earthquake","Flood","Landslide","No-disaster","Wildfire"]

async def predict_disaster(file):
    await file.seek(0)
    image_bytes = await file.read()
    print("Image bytes length:", len(image_bytes))
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((128,128))
    image_array = np.array(image)
    image_array = image_array/255.0
    Final_image = np.expand_dims(image_array,axis=0)
    ##prediction = model.predict(Final_image)[0][0]
    #print("Prediction value:", f"{prediction*100:.2f}%")
    #if prediction > 0.5:
        #return{"Non_Disaster"}
    #else:
        #return{"Disaster"}
    prediction = model.predict(Final_image)
    print("prediction array:", prediction)
    print("max prediction value:", f"{np.max(prediction)*100:.2f}%")
    predicted_class = classes[np.argmax(prediction)]
    print("Predicted class:", predicted_class)
    if predicted_class in ["Earthquake","Flood","Landslide","Wildfire"]:
        return { "Disaster"}
    else:
        return {"Non_Disaster"}
    