import { Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import Feed from './pages/Feed.jsx'
import NavBar from './components/NavBar.jsx'
import Camera from './components/Camera.jsx'
import DisasterUpload from './pages/DisasterUpload.jsx'
import Demo from './pages/Demo.jsx'
import LoginPage from './pages/LoginPage.jsx'
import Grid from './components/Grid.jsx'
import ChatWidget from './components/ChatWidget.jsx'

function App() {
    return (
        
            <Routes>
                <Route path='/' element={
                    <div className='home-page'>
                        
                        <Feed />
                        <NavBar />
                        <ChatWidget />
                        <Camera />
                        <Grid />
                    </div>    
                    
                }
            />

                <Route path='/camera-page' element={<DisasterUpload />}
                />
                <Route path='/upload-form' element={<Demo />}/>
                <Route path='/login-page' element={<LoginPage />} 
                />
            </Routes>
    )
}

export default App
