import { Link } from "react-router-dom";
import "../style/NavBar.css";
import { useNavigate } from "react-router-dom";
import {checkuser} from '../checkuser'
import { useState, useEffect } from "react";

interface User {
    name: string;
    email: string;
    profile_pic: string
}

function NavBar() {
    const navigate = useNavigate()
    const [user, setUser] = useState<User | null>(null)
    const [menu, setMenu] = useState<boolean>(false)
        useEffect(() => {
            async function profile_update(): Promise<void> {
                const auth_response = await checkuser()
                if(auth_response.ok) {
                    const user: User = await auth_response.json()
                    setUser(user)
                }else{
                    setUser(null)
                }
            }
            profile_update()
        },[]);
        
         function logout(): void {
            window.location.href="/api/oauth/logout"
            setUser(null)
        }

        async function demo_page(): Promise<void> {
            const respone = await checkuser()
            if(respone.ok) {
                navigate('/upload-form')
            }else {
                navigate('/login-page')
            }
        }
    return (
        <div className="navbar">
            <div className="nav-left">
                <i className="ti ti-radar"></i>
                <span className="app-title">DisasterWatch</span>
            </div>
    
            <div className="nav-right">
                {/* <Link to="/upload-form" className="btn-demo">Demo</Link> */}
                <button
                    onClick={demo_page} 
                    className='btn-demo'>
                        Demo
                </button>

                <div id="auth-section">
                    {user ? (
                            <div className="profile-container">
                                <img
                                src={user.profile_pic}
                                className="profile-img"
                                id="profile-img"
                                onClick={() =>
                                    setMenu(!menu)
                                    
                                }
                                />
                                {menu && (
                                            <div className="profile-menu"
                                                id="profile-menu">

                                                <div className="profile-info">

                                                    <div className="profile-name">
                                                        {user.name}
                                                    </div>

                                                    <div className="profile-email">
                                                        {user.email}
                                                    </div>
                                                </div>
                                                <button
                                                    className="logout-btn"
                                                    onClick={logout}
                                                >
                                                    Logout
                                                </button>
                                            </div>
                                )}
                                

                            </div>
                        ):(
                            <Link className="btn-login"
                                to={'/login-page'}>
                                    Login / Signup
                            </Link>
                        )}

                </div>

            </div>
        </div>
    );
}
export default NavBar;