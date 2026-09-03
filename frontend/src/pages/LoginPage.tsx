import '../style/LoginPage.css'

function LoginPage() {
       return (
        <div className="login-page">
           <div id="container-login">
                <button onClick={() => window.location.href='api/oauth/login'}
                className="google-btn">
                <img 
                    src="https://img.icons8.com/color/48/000000/google-logo.png" 
                    alt="Google Logo"/>
                <span>Continue with Google</span>
                </button>
            </div>
        </div>    
       )
}
export default LoginPage;