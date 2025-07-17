import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import MouseFollower from './components/MouseFollower';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import { personaPulseAPI } from './services/api';
import './App.css';

function App() {
  const [isDark, setIsDark] = useState(false);
  const [isBackendConnected, setIsBackendConnected] = useState(false);

  useEffect(() => {
    // Check if dark mode is enabled from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDark(true);
      document.documentElement.setAttribute('data-theme', 'dark');
    }

    // Check backend connection
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      await personaPulseAPI.healthCheck();
      setIsBackendConnected(true);
      console.log('Backend connected successfully');
    } catch (error) {
      console.error('Backend connection failed:', error.message);
      setIsBackendConnected(false);
    }
  };

  const toggleTheme = () => {
    const newTheme = !isDark;
    setIsDark(newTheme);
    
    if (newTheme) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
    }
  };

  return (
    <Router>
      <div className={`App ${isDark ? 'dark' : ''}`}>
        <MouseFollower />
        <Navbar isDark={isDark} toggleTheme={toggleTheme} />
        
        {/* Backend Connection Status */}
        {!isBackendConnected && (
          <div className="fixed top-16 left-0 right-0 bg-yellow-100 border-b border-yellow-300 px-4 py-2 text-sm text-yellow-800 text-center z-40">
            ⚠️ Backend connection unavailable. Some features may not work. 
            <button 
              onClick={checkBackendConnection}
              className="ml-2 underline hover:no-underline"
            >
              Retry
            </button>
          </div>
        )}

        <main className="min-h-screen">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;
