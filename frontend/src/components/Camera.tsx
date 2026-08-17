import "../style/Camera.css"
import { useNavigate } from "react-router-dom"
import { checkuser } from "../checkuser";
function Camera(){
    const navigate = useNavigate();
    async function checkUser(): Promise<void> {
        const response = await checkuser()
        if (response.ok) {
            navigate('/camera-page')
        }else {
            navigate('/login-page')
    }
}
    return (
        <div className="camera-fab">
            <button 
                className="fab"
                aria-label="Upload disaster image"
                onClick={checkUser}
            >
                <i className="ti ti-camera"></i>
            </button>
        </div>
    )
}

export default Camera