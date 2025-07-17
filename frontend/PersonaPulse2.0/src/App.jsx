import React, { useState } from 'react';
import axios from 'axios';
import { User, Instagram, Twitter, Linkedin, MessageSquare, Brain, TrendingUp, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [formData, setFormData] = useState({
    instagram: '',
    twitter: '',
    linkedin: '',
    reddit: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Check if at least one social media ID is provided
    const hasAtLeastOne = Object.values(formData).some(value => value.trim() !== '');
    if (!hasAtLeastOne) {
      setError('Please provide at least one social media ID');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      // Filter out empty values
      const socialMediaIds = Object.fromEntries(
        Object.entries(formData).filter(([key, value]) => value.trim() !== '')
      );

      const response = await axios.post(`${API_BASE_URL}/users`, socialMediaIds);
      setResult(response.data);
      
      // Reset form
      setFormData({
        instagram: '',
        twitter: '',
        linkedin: '',
        reddit: ''
      });
    } catch (err) {
      console.error('Error creating user:', err);
      setError(err.response?.data?.error || 'Failed to process your data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="logo">
            <Brain className="logo-icon" />
            <h1>PersonaPulse</h1>
          </div>
          <p className="tagline">Discover Your Digital Personality Through Social Media Analysis</p>
        </header>

        {/* Main Content */}
        <main className="main-content">
          {/* Features Section */}
          <div className="features">
            <div className="feature">
              <TrendingUp className="feature-icon" />
              <h3>Multi-Platform Analysis</h3>
              <p>Analyze your presence across Instagram, Twitter, LinkedIn, and Reddit</p>
            </div>
            <div className="feature">
              <Brain className="feature-icon" />
              <h3>AI-Powered Insights</h3>
              <p>Get OCEAN personality traits and interest keywords using advanced AI</p>
            </div>
            <div className="feature">
              <User className="feature-icon" />
              <h3>Personal Profile</h3>
              <p>Build a comprehensive digital personality profile for better recommendations</p>
            </div>
          </div>

          {/* Form Section */}
          <div className="form-section">
            <h2>Start Your Personality Analysis</h2>
            <p className="form-description">
              Enter your social media usernames/IDs to begin the analysis. At least one platform is required.
            </p>

            <form onSubmit={handleSubmit} className="social-form">
              <div className="input-group">
                <div className="input-wrapper">
                  <Instagram className="input-icon" />
                  <input
                    type="text"
                    name="instagram"
                    placeholder="Instagram username"
                    value={formData.instagram}
                    onChange={handleInputChange}
                    className="social-input"
                  />
                </div>
              </div>

              <div className="input-group">
                <div className="input-wrapper">
                  <Twitter className="input-icon" />
                  <input
                    type="text"
                    name="twitter"
                    placeholder="Twitter username"
                    value={formData.twitter}
                    onChange={handleInputChange}
                    className="social-input"
                  />
                </div>
              </div>

              <div className="input-group">
                <div className="input-wrapper">
                  <Linkedin className="input-icon" />
                  <input
                    type="text"
                    name="linkedin"
                    placeholder="LinkedIn profile URL or username"
                    value={formData.linkedin}
                    onChange={handleInputChange}
                    className="social-input"
                  />
                </div>
              </div>

              <div className="input-group">
                <div className="input-wrapper">
                  <MessageSquare className="input-icon" />
                  <input
                    type="text"
                    name="reddit"
                    placeholder="Reddit username"
                    value={formData.reddit}
                    onChange={handleInputChange}
                    className="social-input"
                  />
                </div>
              </div>

              <button 
                type="submit" 
                disabled={loading}
                className="submit-button"
              >
                {loading ? (
                  <>
                    <Loader className="loading-icon" />
                    Analyzing Your Digital Personality...
                  </>
                ) : (
                  'Start Analysis'
                )}
              </button>
            </form>

            {/* Error Display */}
            {error && (
              <div className="error-message">
                <AlertCircle className="error-icon" />
                <span>{error}</span>
              </div>
            )}

            {/* Success Result */}
            {result && (
              <div className="result-section">
                <div className="success-message">
                  <CheckCircle className="success-icon" />
                  <span>Analysis completed successfully!</span>
                </div>
                
                <div className="result-card">
                  <h3>Your Digital Personality Profile</h3>
                  <div className="result-item">
                    <strong>Unique ID:</strong> {result.data.unique_persona_pulse_id}
                  </div>
                  
                  {result.data.personality_analysis && (
                    <>
                      <div className="result-item">
                        <strong>Interest Keywords:</strong>
                        <div className="keywords">
                          {result.data.personality_analysis.interest_keywords.slice(0, 8).map((keyword, index) => (
                            <span key={index} className="keyword-tag">{keyword}</span>
                          ))}
                        </div>
                      </div>
                      
                      <div className="result-item">
                        <strong>OCEAN Personality Traits:</strong>
                        <div className="ocean-scores">
                          {Object.entries(result.data.personality_analysis.ocean_scores).map(([trait, score]) => (
                            <div key={trait} className="trait-score">
                              <span className="trait-name">{trait.charAt(0).toUpperCase() + trait.slice(1)}</span>
                              <div className="score-bar">
                                <div 
                                  className="score-fill" 
                                  style={{ width: `${score}%` }}
                                ></div>
                              </div>
                              <span className="score-value">{score}/100</span>
                            </div>
                          ))}
                        </div>
                      </div>
                      
                      <div className="result-item">
                        <strong>Confidence Score:</strong> {result.data.personality_analysis.confidence_score}/100
                      </div>
                    </>
                  )}
                  
                  <div className="result-item">
                    <strong>Platforms Analyzed:</strong>
                    <div className="platforms-status">
                      {Object.entries(result.data.scraping_results).map(([platform, success]) => (
                        <span 
                          key={platform} 
                          className={`platform-status ${success ? 'success' : 'failed'}`}
                        >
                          {platform.charAt(0).toUpperCase() + platform.slice(1)}: {success ? '✓' : '✗'}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Loading State */}
            {loading && (
              <div className="loading-section">
                <div className="loading-steps">
                  <div className="loading-step">
                    <Loader className="step-icon" />
                    <span>Scraping social media data...</span>
                  </div>
                  <div className="loading-step">
                    <Brain className="step-icon" />
                    <span>Analyzing personality with AI...</span>
                  </div>
                  <div className="loading-step">
                    <CheckCircle className="step-icon" />
                    <span>Generating insights...</span>
                  </div>
                </div>
                <p className="loading-note">This process may take 2-3 minutes depending on the amount of data.</p>
              </div>
            )}
          </div>
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>&copy; 2025 PersonaPulse. Discover your digital personality through AI-powered social media analysis.</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
