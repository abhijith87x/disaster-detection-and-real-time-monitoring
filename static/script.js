var imageCapture;
if(window.location.pathname.includes("/input-camera")) {
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
            const accuracy = position.coords.accuracy
            if ( accuracy > 20){
                alert("Location accuracy is low! Use your smartphone to get high accuracy")
            }
            formData.append("latitude", latitude);
            formData.append("longitude", longitude);
            console.log("location appended",latitude,longitude,accuracy);
            resolve(formData);
        },
        (error) => {
            console.error("Error getting geolocation:", error.code,error.message);
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
   
    if (lat && lon) {
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
    return  fetch("http://localhost:8000/profile",{
      method : 'GET',
      credentials: 'include'
  });
}

async function profile_update() {
const auth_response = await checkuser();
const authSection = document.getElementById("auth-section");
const authButton =  document.getElementById("auth-section");
console.log("auth button : ",authButton)
if(auth_response.ok) {
  const user = await auth_response.json()
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

async function senddata() {
    response = await fetch("http://localhost:8000/upload-data", {
    method: "POST",
    body: formData,
    credentials: 'include'
})

console.log("response : ",response)
const data = await response.json();
if(response.status == 401) {
    window.location.href="/login-page"
}else if(data == "Non_Disaster") {
    alert("Given image is not Disaster...Reupload");
}else if(data == "Screen_captured_image") {
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

function upload() {
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
      console.log("disaster")
      //alert("Successfully Uploaded for Backend Process");
      //window.location.href="/"
    }else{
      window.location.href="/login-page"
    }
})
.catch(err => console.error("error : ", err))
}

/* ═══════════════════════════════════════════════
   DisasterWatch — script.js
   ═══════════════════════════════════════════════ */
console.log("script loadedddddddddd");
const socket = io("http://localhost:8000");  // connect to WebSocket server
console.log("socket : soc")

/* ─────────────────────────────────────────
   LIKE
   ───────────────────────────────────────── */
async function lk(btn, cardId, id) {
    const response = await checkuser();
    if(response.ok) {
        user = await response.json();
        if(user) {
            currentUserId = user.id;
            console.log("card id",cardId,typeof(cardId))
            let like = false;
            const card_id = document.getElementById(cardId);
            const isOn  = btn.classList.contains('lk-on');
            if (card_id.classList.contains('dk-on')) {
                card_id.classList.remove('dk-on');
                void card_id.offsetWidth;
            }
            btn.classList.remove('lk-on');
            void btn.offsetWidth;
            if(!isOn) {
                btn.classList.add('lk-on');
                like = true;
            }
    
            console.log("current user id : ",currentUserId)
            //const card_iid = parseInt(cardId.substring(1))
            fetch(`http://localhost:8000/user/like/update?current_user=${currentUserId}&card_id=${id}&like=${like}`,{
                method : "POST"
            });
        }else{
            window.location.href="/login-page"
        }
    }else{
        window.location.href="/login-page"
    }
}


/* ────────────────────────────────────────
   DISLIKE
   ───────────────────────────────────────── */
const dislikeReasons = [
    'Flood',
    'Landslide',
    'Earthquake',
    'Wildfire',
    'Tsunami'
];
 
let pendingDislike = { btn: null, cardId: null, id: null, dislike : null, type : null };

async function dk(btn, cardId, id, type) {
    const response = await checkuser();
        if(response.ok) {
            user = await response.json();

            if(user) {
                let dislike = false
                if (btn.classList.contains('dk-on')) {
                    btn.classList.remove('dk-on');
                    void btn.offsetWidth;
                    currentUserId = user.id;
                    fetch(`http://localhost:8000/user/dislike/update?current_user=${currentUserId}&card_id=${id}&dislike=${dislike}&type=${type}`,{
                        method : "POST"
                    });
                    return;
                }

                pendingDislike = { btn, cardId, id, dislike : true, type };
                console.log(pendingDislike)
                openDislikePopup();   

           }else{
                window.location.href="/login-page"
            }
        }else{
            window.location.href="/login-page"
        }
}

function openDislikePopup() {
    //closeDislikePopup(); // remove any existing one first
 
    const overlay = document.createElement('div');
    overlay.className = 'dislike-overlay';
    overlay.id = 'dislikeOverlay';
 
    const optionsHTML = dislikeReasons.map((reason, i) => `
        <label class="dislike-option">
            <input type="radio" name="dislikeReason" value="${reason}" ${i === 0 ? 'checked' : ''}>
            <span>${reason}</span>
        </label>
    `).join('');
 
    overlay.innerHTML = `
        <div class="dislike-box">
            <h3 class="dislike-title">What type of disaster is this?</h3>
            <div class="dislike-options">
                ${optionsHTML}
            </div>
            <div class="dislike-actions">
                <button class="dislike-cancel" onclick="closeDislikePopup()">Cancel</button>
                <button class="dislike-submit" onclick="confirmDislike()">Submit</button>
            </div>
        </div>`;
 
    document.body.appendChild(overlay);
}
 
function closeDislikePopup() {
    const existing = document.getElementById('dislikeOverlay');
    if (existing) existing.remove();
    pendingDislike = { btn: null, cardIdId: null, id: null, dislike : null, type : null };
}
 
async function confirmDislike() {
    console.log("startednpop")
    const response = await checkuser();
        if(response.ok) {
            user = await response.json();

            if(user) {
                currentUserId = user.id;
                const selected = document.querySelector('input[name="dislikeReason"]:checked');
                pendingDislike.type = selected.value
                if (!selected) {
                    alert("Empty respone");
                        return
                    }
                
                const { btn, cardId, id, dislike, type } = pendingDislike;
                console.log(btn, cardId)
                if (!btn) return;
 
                const other = document.getElementById(cardId);
                if (other && other.classList.contains('lk-on')) {
                    other.classList.remove('lk-on');
                    void other.offsetWidth;
                }
    
                btn.classList.remove('dk-on');
                void btn.offsetWidth;
                btn.classList.add('dk-on');
               
                fetch(`http://localhost:8000/user/dislike/update?current_user=${currentUserId}&card_id=${id}&dislike=${dislike}&type=${type}`,{
                        method : "POST"
                });
                console.log("after fetch")
                closeDislikePopup();
            }else{
                window.location.href="/login-page"
            }
        }else{
            window.location.href="/login-page"
        }
}

/* ─────────────────────────────────────────
   REPORT
   ───────────────────────────────────────── */
async function rpt(btn, cardId) {
    console.log("card id",cardId)
    const response = await checkuser();
        if(response.ok) {
            user = await response.json();
            if(user) {
                let report = true
                currentUserId = user.id;
                console.log("current user id : ",currentUserId)
                const card_id = parseInt(cardId.substring(1))
                if (btn.classList.contains('reported')){
                    btn.classList.remove('reported');
                    btn.textContent = 'Report';
                    report = false
                }else{
                    btn.classList.add('reported')
                    btn.textContent = 'Reported';
                }
                fetch(`http://localhost:8000/user/report/update?current_user=${currentUserId}&card_id=${card_id}&report=${report}`,{
                    method : "POST"
                });
           }else{
                window.location.href="/login-page"
            }
    }else{
        window.location.href="/login-page"
    }
}


/* ─────────────────────────────────────────
   THREE-DOT
   ───────────────────────────────────────── */
function om(tdId) {
    const dd  = document.getElementById(tdId).querySelector('.ddrop');
    const was = dd.classList.contains('open');
    document.querySelectorAll('.ddrop').forEach(d => d.classList.remove('open'));
    if (!was) dd.classList.add('open');
}

document.addEventListener('click', function (e) {
    if (!e.target.closest('.tdwrap')) {
        document.querySelectorAll('.ddrop').forEach(d => d.classList.remove('open'));
    }
});


/* ─────────────────────────────────────────
   DELETE CARD
   ───────────────────────────────────────── */
async function del(cardId) {
    const response = await checkuser();
    if(response.ok) {
        user = await response.json();
        if(user) {
            const currentUserId = user.id
            const card_id = cardId.replace('c', '');
            fetch(`/user/reports/delete?card_id=${card_id}&currentUserId=${currentUserId}`, { method: 'DELETE' })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    removeCard(card_id);
                    document.querySelectorAll('.ddrop').forEach(d => d.classList.remove('open'));
                }
            });
        } else {
            window.location.href="/login-page"
        }
    } else {
        window.location.href="/login-page"
    }
}


/* ─────────────────────────────────────────
   REMOVE CARD FROM DOM
   used by both delete and websocket
   ───────────────────────────────────────── */
function removeCard(reportId) {
    const card = document.getElementById('c' + reportId);
    if (card) {
        card.style.transition = 'opacity 0.25s';
        card.style.opacity    = '0';
        setTimeout(() => card.remove(), 260);
    }
}


/* ═══════════════════════════════════════════════
   createCard(report, canDelete)
   ───────────────────────────────────────────────
   report = {
       id        : unique id           (string | number)
       type      : 'fire'|'flood'|'quake'|'wind'
       caption   : string              (fully from backend)
       image_url : string | null       (null shows placeholder)
   }
   canDelete = true   → three-dot with Delete renders
   canDelete = false  → no three-dot at all
   ═══════════════════════════════════════════════ */
 async function createCard(report, canDelete, user_actions) {
    const id = report.image_id;
    const latitude = report.latitude;
    const longitude = report.longitude;
    /* prevent duplicate if card already on screen */
    if (document.getElementById('c' + id)) return;

    /* image from backend or placeholder */
    const imageHTML = report.image_path
        ? `<img src="http://127.0.0.1:8000/${report.image_path}" class="cimg" alt="Disaster photo">`
        : `<div class="cimg-placeholder"><i class="ti ti-photo"></i></div>`;

    /* caption 100% from backend */
    const caption = report.description || '';

    /* burst particles for like/dislike animation */
    const burst = `
        <span class="burst-wrap">
            <span class="b b1"></span>
            <span class="b b2"></span>
            <span class="b b3"></span>
            <span class="b b4"></span>
            <span class="b b5"></span>
            <span class="b b6"></span>
        </span>`;

    /* three-dot only when canDelete is true */
    const threeDot = canDelete ? `
        <div class="tdwrap" id="td${id}">
            <button class="tdbtn" onclick="om('td${id}')" aria-label="More options">
                <i class="ti ti-dots-vertical"></i>
            </button>
            <div class="ddrop" id="dd${id}">
                <button onclick="del('c${id}')">
                    <i class="ti ti-trash"></i> Delete
                </button>
            </div>
        </div>` : '';

    /* full card html */
    const cardHTML = `
        <div class="dcard" id="c${id}">
            <div class="cimg-slot">${imageHTML}</div>
            <div class="cbody">
                <span class="ctag ${report.status}">${report.status}</span>
                <p class="ccap">${caption}</p>
                <div class="cacts">
                    <button class="abtn" id="l${id}" onclick="lk(this, 'd${id}', '${id}')" aria-label="Confirm">
                        ${burst}<i class="ti ti-thumb-up"></i>
                    </button>
                    <button class="abtn" id="d${id}" onclick="dk(this, 'l${id}', '${id}')" aria-label="Doubt">
                        ${burst}<i class="ti ti-thumb-down"></i>
                    </button>
                    <button class="loc-btn" id="loc${id}" onclick="openLocation('${latitude}', '${longitude}')" aria-label="Location">
                        <i class="ti ti-map-pin"></i>
                    </button>
                    <div class="sp"></div>
                    <button class="rpt-btn" id="r${id}" onclick="rpt(this, 'r${id}')">Report</button>
                    ${threeDot}
                </div>
            </div>
        </div>`;
        

    /* newest card at top of feed */
    document.getElementById('disaster-feed').insertAdjacentHTML('afterbegin', cardHTML);
    // const feed = await document.getElementById('disaster-feed');
     //console.log("feed =", feed);
     //feed.insertAdjacentHTML('beforeend', cardHTML);
    if (user_actions && user_actions.reaction == "LIKE"){
            const card_id = document.getElementById(`l${id}`);
            console.log("cardddd", card_id)
            card_id.classList.add('lk-on');
        }

    if (user_actions && user_actions.reaction == "DISLIKE") {
        const card_id = document.getElementById(`d${id}`);
            console.log("cardddd", card_id)
            card_id.classList.add('dk-on');
        }

    if (user_actions && user_actions.reported == "TRUE") {
        const card_id = document.getElementById(`r${id}`);
        console.log("report  cardddd", card_id)
        card_id.textContent = 'reported'
    }
 }

/* ═══════════════════════════════════════════════
   WEBSOCKET EVENTS
   ═══════════════════════════════════════════════ */

/* new report from anyone → appears instantly on all screens */
socket.on('new_report', async function(report) {
    console.log("my_reporttt",report)
    const feed = document.getElementById("disaster-feed");
    if (!feed) {
        return;
    }
    const response = await checkuser();
    console.log("after checkuser")
    if (response.ok){
        user = await response.json();
           if(user){
                currentUserId = user.id;
                console.log("current user id : ",currentUserId)
           }else{
                currentUserId = "";
            }
    }
    const canDelete = (report.user_id === currentUserId);
    console.log("socket report",report)
    await createCard(report, canDelete);
});

/* report deleted by owner → disappears instantly on all screens */
socket.on('remove_report', function(card_id) {
    removeCard(card_id);
});

socket.on('status_update', function(status){
    element = document.getElementById("c" + status.card_id).querySelector(".ctag")
    element.textContent = status.status
    element.className = `ctag ${status.status}`;
})

socket.on('update_description', function(data){
    element = document.getElementById("c" + data.card_id).querySelector(".ccap")
    element.textContent = data.description
})

/* ═══════════════════════════════════════════════
   PAGE LOAD
   fetch latest reports from MySQL on every load
   ═══════════════════════════════════════════════ */
let page = 1;
let currentUserId ="";
const user_action_map = {}
async function loadReports() {
    const res = await fetch(`/feed/reports/latest?page=${page}`)
        reports = await res.json()
        //.then(res => res.json())
        //.then(reports => {
        if (reports.length === 0) {
            return;
        }
        const response = await checkuser();
        if (response.ok){
            user = await response.json();
            if(user){
                currentUserId = user.id;
                const user_actions =  await fetch(`/feed/card/action?currentUser=${currentUserId}`)
                if (user_actions.ok){
                    const user_action = await user_actions.json()
                    if (user_action) {
                        user_action.forEach(action => {
                            user_action_map[action.card_id] = action
                        })
                    }
                }
           }else{
                currentUserId = "";
            }
        }
        ////////
        reports.forEach(report => {   
            console.log(report) 
            const user_actions = user_action_map[report.image_id]
            can_delete = (report.user_id === currentUserId);
            console.log("kkkkkkk",report.status)
            const  reaction = "Like"
            createCard(report, can_delete, user_actions);
            });
            page++;
        //});
    }
if (window.location.pathname === "/") {
loadReports();
console.log("executd")
}

/* load more when user scrolls to bottom */
if (window.location.pathname === "/") {
window.addEventListener('scroll', function () {
    const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
    if (nearBottom) loadReports();
});
}

function openLocation(latitude, longitude){
    window.open(`https://www.google.com/maps?q=${latitude},${longitude}`, '_blank')
}