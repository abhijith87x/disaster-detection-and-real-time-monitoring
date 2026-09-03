import { useState } from "react";
import "../style/Demo.css"
import { useNavigate } from "react-router-dom";

function Demo() {

    const navigate = useNavigate()

    const [image, setImage] = useState<File | null>(null); 
    const [preview, setPreview] = useState<string | null>(null)

    function appendGeolocationToFormData(formData: FormData) {
    return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
        function (position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const accuracy = position.coords.accuracy;
            if ( accuracy > 20){
                alert("Location accuracy is low! Use your smartphone to get high accuracy")
            }
            formData.append("latitude", latitude.toString());
            formData.append("longitude", longitude.toString());
            resolve(formData);
        },
        (error) => {
            alert("turn on the location for upload");
            // You might still want to resolve with the original formData if geolocation isn't critical
             // or reject if it's essential.
            resolve(formData); 
        },
        {
          enableHighAccuracy :true,
          timeout:40000,
          maximumAge:60000
        }
    );
    } else {
        alert("Geolocation is not supported by this browser.");
        resolve(formData); // Resolve with original formData if geolocation is not supported
    }
  });
}
   
    function preview_image(
        event: React.ChangeEvent<HTMLInputElement>
    ) {
    console.log("going")
        const file = event.target.files?.[0];
        if (file) { 
            setImage(file)
            setPreview(URL.createObjectURL(file));
        }

    }
    
    async function upload(): Promise<void> {
        if (!image) {
            alert("Please give file and location for upload");
            return;
        }

        const demo_formData = new FormData()
        await appendGeolocationToFormData(demo_formData)
        demo_formData.append("File", image)
        const latitude = demo_formData.get("latitude");
        const longitude = demo_formData.get("longitude");
        console.log("laatitiude",latitude,longitude)
        if (!image || !latitude || !longitude ){
            alert("Please give file and location for upload")
            return;
        }
        console.log("executredddd")
        const response = await fetch("/api/disaster/demo",{
            
            method:"POST",
            body : demo_formData,
            credentials: 'include',
        })
        .then(res => res.json())
        .then(data => {
            if (data == "Non_Disaster"){
                alert("Given image is not Disaster...Reupload");
            }else if (data == "Disaster already reported in this area."){
                alert("A disaster of the same type has already been reported in this area.");
            }else if (data == "Disaster"){
                alert("Successfully Uploaded for Backend Process");
                navigate('/')
            }else{
                navigate('/login-page')
            }
        })
        .catch(err => console.error("error : ", err))
        } 

    return (
      <div className="form">
        <h1 id="demo-tag">Upload Disaster Image</h1>
            <input 
                type="file"
                accept="image/*"
                onChange={preview_image}
             />   

            {
                preview && (
                    <img
                        src={preview}
                        width={350} 
                        alt="preview"     
                    />
                )       
            }

            <button
                type="button"
                onClick={upload}
                >
                    upload
            </button>  
        </div>
    )
}
export default Demo;