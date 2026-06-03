var imageCapture;
if (window.location.pathname.includes("/input-camera")){
navigator.mediaDevices.getUserMedia({ video: true })
  .then(mediaStream => {
  document.querySelector('video').srcObject = mediaStream
  const track = mediaStream.getVideoTracks()[0];
  imageCapture = new ImageCapture(track);
})
  .catch(error => alert("allow camera permission")
 );
}

function grabFrameButton() {
  imageCapture.grabFrame()
  .then(imageBitmap => {
  const canvas = document.querySelector('#grabFrameCanvas');
  drawCanvas(canvas, imageBitmap);
  })
  .catch(error => console.log(error));
};

function appendGeolocationToFormData(formData) {
    return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      console.log("starting")
      navigator.geolocation.getCurrentPosition(
        function (position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        formData.append("latitude", latitude);
        formData.append("longitude", longitude);
        console.log("location appended");
        resolve(formData); // Resolve with the updated FormData

        //document.getElementById("upload").style.display="block";
      },
        (error) => {
          console.error("Error getting geolocation:", error.code,error.message);
          alert("turn on the location for upload");
          // You might still want to resolve with the original formData if geolocation isn't critical
          // or reject if it's essential.
          resolve(formData); 
        },
        {
          enableHighAccuracy :false,
          timeout:40000,
          maximumAge:60000
        }
      );
    } else {
      console.warn("Geolocation is not supported by this browser.");
      resolve(formData); // Resolve with original formData if geolocation is not supported
    }
  });
}

 let date,formData;
 function takePhotoButton() {
  imageCapture.takePhoto()
  .then(blob => createImageBitmap(blob))
  .then(imageBitmap => {
    const canvas = document.querySelector('#takePhotoCanvas');
    drawCanvas(canvas, imageBitmap);
    let base64String = canvas.toDataURL("img/png");
    //if (base64String){
       //document.getElementById("upload").style.display="block";
    //}
    const contentType = base64String.split(';')[0].split(':')[1]; // Extract MIME type
    const blob = base64ToBlob(base64String, contentType);
    function base64ToBlob(base64, contentType) {
        const sliceSize = 512;
        const byteCharacters = atob(base64.split(',')[1]); // Decode base64
        const byteArrays = [];

        for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            const slice = byteCharacters.slice(offset, offset + sliceSize);
            const byteNumbers = new Array(slice.length);
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
          }
        return new Blob(byteArrays,{ type: contentType });
      } 
     formData = new FormData();
     formData.append("file", blob,"captured_media.png");
    //console.log("blob",blob)
    date = new Date().toISOString().split("T")[0];//.toLocaleString();//
    formData.append("date",date);
    console.log("date is appended")
    console.log(typeof(date))
    appendGeolocationToFormData(formData)
    
console.log("hello");
appendGeolocationToFormData(formData)
.then(updatedFormData => { 
    lat = updatedFormData.get("latitude");
    lon = updatedFormData.get('longitude');
    file = updatedFormData.get('file');
    date = updatedFormData.get('date')
    console.log("values",file)
    console.log(typeof(lon))
    //console.log(file)
    //console.log( typeof lat);
   
    if (lat && lon){
      console.log("this oky");
      document.getElementById("upload").style.display="block";
  
    }  
    })
    .catch((error) => {
       console.error("Error getting geolocation:", error);
    });
   appendGeolocationToFormData(formData).then(updatedFormData => {
   for (let pair of updatedFormData.entries()) {
   console.log(pair[0] + ': ' + pair[1]);
  }
});
   //async function uploadformData() {
    //const lat = await appendGeolocationToFormData(formData);
    //console.log(updatedFormData.get('longitude')); // e.g., 76.7890
//}

  })
  .catch(error => console.log(error));
};


/* Utils */

function drawCanvas(canvas, img) {
  canvas.width = getComputedStyle(canvas).width.split('px')[0];
  canvas.height = getComputedStyle(canvas).height.split('px')[0];
  let ratio  = Math.min(canvas.width / img.width, canvas.height / img.height);
  let x = (canvas.width - img.width * ratio) / 2;
  let y = (canvas.height - img.height * ratio) / 2;
  canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
  canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height,
      x, y, img.width * ratio, img.height * ratio);
};

async function checkuser() {
      const response = await fetch("http://localhost:8000/profile",{
      method : 'GET',
      credentials: 'include'
  });
  
const authSection = document.getElementById("auth-section");
const authButton =  document.getElementById("auth-section");
console.log("auth button : ",authButton)
if (response.ok){
  const user = await response.json()
  if (user) {
    authSection.innerHTML = `
            <div class="profile-container">

                <img
                    src="${user.profile_pic}"
                    class="profile-img"
                    id="profile-img"
                >

                <div class="profile-menu"
                    id="profile-menu">

                    <div class="profile-info">

                        <div class="profile-name">
                            ${user.name}
                        </div>

                        <div class="profile-email">
                            ${user.email}
                        </div>

                    </div>

                    <button
                        class="logout-btn"
                        onclick="window.location.href='/logout'"
                    >
                        Logout
                    </button>

                </div>

            </div>
            `;

            const profileImg =
                document.getElementById("profile-img");

            const profileMenu =
                document.getElementById("profile-menu");

            profileImg.addEventListener("click", () => {

                if (
                    profileMenu.style.display === "block"
                ) {

                    profileMenu.style.display = "none";

                } else {

                    profileMenu.style.display = "block";
                }

            });

        }
}else{
  authSection.innerHTML = `
    <button class="btn-login"
        onclick="window.location.href='/login-page'">
        Login / Signup
    </button>
    `;
 }
}
async function senddata(){
  //console.log(file,"...",typeof(file),"....",file instanceof File)
  //const reader = new FileReader();
  //reader.onload = (e)=>{
    //const img = document.createElement("img");
    //img.src = e.target.result
    //img.style.width = "200px"
    //document.body.appendChild(img)
  //}
  //reader.readAsDataURL(file)
   //url = URL.createObjectURL("file");
     //window.open(url,"_blank")
  //console.log("button clicked",date)
  //const formdata = new FormData()
  //formdata.append("latitude",lat)
  //formdata.append("longitude",lon)
  //formdata.append("file",file)
  //formdata.append("date",date)
  //formdata.append("name","abhi")
  response = await fetch("http://localhost:8000/upload-data", {
    method: "POST",
    body: formData,
    credentials: 'include'
  })
  console.log("response : ",response)
  const data = await response.json();
  if (response.status == 401){
    window.location.href="/login-page"
  }else if (data == "Non_Disaster"){
    alert("Given image is not Disaster...Reupload");
  }else if (data == "Screen_captured_image"){
    alert("Sorry Not uploaded! Image is fake or manipulated");
}else{
    alert("Successfully Uploaded for Backend Process");
  }
  //.then(res => res.json())
  //.then(data =>{
    //console.log("data : ",data.status_code)
    //if (data == "Screen_captured_image"){
      //alert("Sorry Not uploaded! Image is fake or manipulated");
    //}else if( data == "Disaster"){
      //alert("Successfully Uploaded within few Minutes")
      //window.location.href = "/"
    //}else{
      //alert("Your image looking Non Disaster..Reupload");
    //}
  //})
  //.catch(err => console.error("Error:", err));
  
}
//FOR DEMO PAGE
let demo_file;
const demo_formdata = new FormData();
function preview_image(event){
  appendGeolocationToFormData(demo_formdata)
  demo_file = event.target.files[0];
  img = document.getElementById("preview");
  img.src = URL.createObjectURL(demo_file);
  
}
function upload(){
  latitude = demo_formdata.get("latitude")
  longitude = demo_formdata.get("longitude");
  console.log(latitude,longitude)
  if (!demo_file || !latitude || !longitude ){
    alert("Please give file and location for upload")
    return;
  }
  demo_formdata.append("File",demo_file);
  demo_formdata.append("latitude",latitude);
  demo_formdata.append("longitude",longitude);
  console.log("success : ",demo_formdata);
    fetch("http://localhost:8000/demo",{
      method:"POST",
      body : demo_formdata,
      credentials: 'include'
  })

.then(res => res.json())
.then(data => {
    if (data == "Non_Disaster"){
      alert("Given image is not Disaster...Reupload");
    }else if (data == "Disaster"){
      console.log("data : ",data);
      alert("Successfully Uploaded for Backend Process");
      window.location.href="/"
    }else{
      window.location.href="/login-page"
    }
})
.catch(err => console.error("error : ",err))
}


