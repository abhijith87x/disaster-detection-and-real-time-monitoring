
import { useEffect, useRef } from "react";
import "../style/DisasterUpload.css";

let formData;

function DisasterUpload() {

    const imageCaptureRef = useRef(null);
    const videoRef = useRef(null);

    useEffect(() => {

        let mediaStream;

        navigator.mediaDevices.getUserMedia({
            video: true
            // or:
            // video: { facingMode: "environment" }
        })
        .then((stream) => {

            mediaStream = stream;

            // Show camera stream in video
            videoRef.current.srcObject = stream;

            // Get camera track
            const track = stream.getVideoTracks()[0];

            // Create ImageCapture
            imageCaptureRef.current = new ImageCapture(track);

        })
        .catch(() => {
            alert("Allow camera permission");
        });

        // Cleanup when component unmounts
        return () => {

            if (mediaStream) {

                mediaStream.getTracks().forEach((track) => {
                    track.stop();
                });

            }

            // Remove video stream
            if (videoRef.current) {
                videoRef.current.srcObject = null;
            }

        };

    }, []);


    function takePhotoButton() {

        imageCaptureRef.current
            .takePhoto()

            .then((blob) => {

                return createImageBitmap(blob)
                    .then((imageBitmap) => ({
                        blob,
                        imageBitmap
                    }));

            })

            .then(({ blob, imageBitmap }) => {

                const canvas =
                    document.querySelector("#takePhotoCanvas");

                drawCanvas(canvas, imageBitmap);

                formData = new FormData();

                formData.append(
                    "file",
                    blob,
                    "captured_media.png"
                );

                const date = new Date()
                    .toISOString()
                    .split("T")[0];

                formData.append("date", date);

                appendGeolocationToFormData(formData)

                    .then((updatedFormData) => {

                        const lat =
                            updatedFormData.get("latitude");

                        const lon =
                            updatedFormData.get("longitude");

                        const file =
                            updatedFormData.get("file");

                        const uploadDate =
                            updatedFormData.get("date");

                        console.log(
                            lat,
                            lon,
                            file,
                            uploadDate
                        );

                        if (lat && lon) {

                            document.getElementById(
                                "upload"
                            ).style.display = "block";

                        }

                    })

                    .catch((error) => {
                        console.error(error);
                    });

            })

            .catch((error) => {
                console.error(error);
            });

    }


    function appendGeolocationToFormData(formData) {

        return new Promise((resolve) => {

            if (navigator.geolocation) {

                navigator.geolocation.getCurrentPosition(

                    (position) => {

                        const latitude =
                            position.coords.latitude;

                        const longitude =
                            position.coords.longitude;

                        const accuracy =
                            position.coords.accuracy;

                        if (accuracy > 20) {

                            alert(
                                "Location accuracy is low! Use your smartphone."
                            );

                        }

                        formData.append(
                            "latitude",
                            latitude
                        );

                        formData.append(
                            "longitude",
                            longitude
                        );

                        resolve(formData);

                    },

                    () => {

                        alert("Turn on location.");

                        resolve(formData);

                    },

                    {
                        enableHighAccuracy: true,
                        timeout: 40000,
                        maximumAge: 60000
                    }

                );

            }

            else {

                alert(
                    "Geolocation not supported."
                );

                resolve(formData);

            }

        });

    }


    function drawCanvas(canvas, img) {

        canvas.width =
            parseInt(
                getComputedStyle(canvas).width
            );

        canvas.height =
            parseInt(
                getComputedStyle(canvas).height
            );

        const ratio = Math.min(

            canvas.width / img.width,

            canvas.height / img.height

        );

        const x =
            (canvas.width - img.width * ratio) / 2;

        const y =
            (canvas.height - img.height * ratio) / 2;

        const ctx =
            canvas.getContext("2d");

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        ctx.drawImage(

            img,

            0,
            0,

            img.width,
            img.height,

            x,
            y,

            img.width * ratio,
            img.height * ratio

        );

    }


    async function senddata() {

        console.log("worked");

        const response = await fetch(
            "/upload-data",
            {
                method: "POST",
                body: formData,
                credentials: "include"
            }
        );

        const data =
            await response.json();

        if (response.status === 401) {

            window.location.href =
                "/login-page";

        }

        else if (data === "Non_Disaster") {

            alert(
                "Given image is not Disaster...Reupload"
            );

        }

        else if (
            data === "Screen_captured_image"
        ) {

            alert(
                "Sorry Not uploaded! Image is fake or manipulated"
            );

        }

        else {

            alert(
                "Successfully Uploaded for Backend Process"
            );

        }

    }


    return (

        <>

            <video
                ref={videoRef}
                id="video"
                autoPlay
                playsInline
            />

            <button
                id="start-button"
                onClick={takePhotoButton}
            >
                Capture photo
            </button>

            <button
                id="upload"
                style={{ display: "none" }}
                onClick={senddata}
            >
                Upload
            </button>

            <canvas
                id="takePhotoCanvas"
            />

        </>

    );

}

export default DisasterUpload;
