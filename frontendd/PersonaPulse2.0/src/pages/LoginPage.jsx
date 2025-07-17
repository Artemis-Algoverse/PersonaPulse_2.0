import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    instagram: '',
    twitter: '',
    linkedin: '',
    reddit: ''
  });
  const [loading, setLoading] = useState(false);
  const [isSignup, setIsSignup] = useState(true);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Login user
      login(formData);
      
      // Navigate to loading page
      navigate('/loading');
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBackToHome = () => {
    navigate('/');
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <button onClick={handleBackToHome} className="back-button">
          ← Back to Home
        </button>
        
        <div className="login-header">
          <h1>PersonaPulse</h1>
          <h2>{isSignup ? 'Join PersonaPulse' : 'Welcome Back'}</h2>
          <p>{isSignup ? 'Enter your social media profiles to get started' : 'Sign in to your account'}</p>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Enter your full name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="Enter your email"
            />
          </div>

          <div className="social-media-section">
            <h3>Connect Your Social Media</h3>
            <p>Link your profiles for personality analysis</p>
            
            <div className="form-group">
              <label htmlFor="instagram">
                <span className="social-icon">📷</span>
                Instagram Username
              </label>
              <input
                type="text"
                id="instagram"
                name="instagram"
                value={formData.instagram}
                onChange={handleChange}
                placeholder="@username"
              />
            </div>

            <div className="form-group">
              <label htmlFor="twitter">
                <span className="social-icon">🐦</span>
                Twitter/X Username
              </label>
              <input
                type="text"
                id="twitter"
                name="twitter"
                value={formData.twitter}
                onChange={handleChange}
                placeholder="@username"
              />
            </div>

            <div className="form-group">
              <label htmlFor="linkedin">
                <span className="social-icon">💼</span>
                LinkedIn Profile
              </label>
              <input
                type="text"
                id="linkedin"
                name="linkedin"
                value={formData.linkedin}
                onChange={handleChange}
                placeholder="linkedin.com/in/username"
              />
            </div>

            <div className="form-group">
              <label htmlFor="reddit">
                <span className="social-icon">🔴</span>
                Reddit Username
              </label>
              <input
                type="text"
                id="reddit"
                name="reddit"
                value={formData.reddit}
                onChange={handleChange}
                placeholder="u/username"
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
            {loading ? 'Processing...' : 'Start Analysis'}
          </button>
          
          <div className="form-footer">
            <p>
              {isSignup ? 'Already have an account?' : 'Don\'t have an account?'}
              <button 
                type="button" 
                onClick={() => setIsSignup(!isSignup)}
                className="link-button"
              >
                {isSignup ? 'Sign In' : 'Sign Up'}
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;