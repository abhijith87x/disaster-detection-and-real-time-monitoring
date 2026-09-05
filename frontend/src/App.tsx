import { Routes, Route } from "react-router-dom";

import "./App.css";

import Feed from "./pages/Feed";
import NavBar from "./components/NavBar";
import Camera from "./components/Camera";
import DisasterUpload from "./pages/DisasterUpload";
import Demo from "./pages/Demo";
import LoginPage from "./pages/LoginPage";
import Grid from "./components/Grid";
import ChatWidget from "./components/ChatWidget";

function App() {
    alert("Welcome to the Disaster Management System! Use the camera icon at the bottom right to upload real disaster images. Use the Demo button at the top right for testing and demonstration purposes, since real disaster incidents cannot be created for testing. ");
    return (
        <Routes>
            <Route
                path="/"
                element={
                    <div className="home-page">
                        <Feed />
                        <NavBar />
                        <ChatWidget />
                        <Camera />
                        <Grid />
                    </div>
                }
            />

            <Route
                path="/camera-page"
                element={<DisasterUpload />}
            />

            <Route
                path="/upload-form"
                element={<Demo />}
            />

            <Route
                path="/login-page"
                element={<LoginPage />}
            />
        </Routes>
    );
}

export default App;