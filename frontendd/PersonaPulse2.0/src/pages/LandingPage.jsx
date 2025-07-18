import './LandingPage.css';
import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <nav className="navbar">
        <div className="logo">PersonaPulse</div>
        <div className="nav-buttons">
          <Link to="/login" className="btn btn-secondary">Login</Link>
          <Link to="/signup" className="btn btn-primary">Sign Up</Link>
        </div>
      </nav>

      <section className="hero">
        <h1 style={{ color: '#000' }}>Discover Your Digital Personality</h1>
        <p style={{ color: '#000' }}>
          Unlock insights into your personality through AI-powered analysis of your social media presence. 
          Get personalized recommendations for events, connections, and growth opportunities.
        </p>
        <Link to="/signup" className="btn btn-primary btn-large" style={{ color: '#ff9966' }}>Get Started</Link>
      </section>

      <section className="features">
        <div className="feature-card">
          <h3 style={{ color: '#000' }}>AI-Powered Analysis</h3>
          <p style={{ color: '#000' }}>Advanced algorithms analyze your social media activity to understand your personality traits using the Big Five model.</p>
        </div>
        <div className="feature-card">
          <h3 style={{ color: '#000' }}>Personalized Recommendations</h3>
          <p style={{ color: '#000' }}>Get tailored event suggestions and networking opportunities based on your unique personality profile.</p>
        </div>
        <div className="feature-card">
          <h3 style={{ color: '#000' }}>Privacy First</h3>
          <p style={{ color: '#000' }}>Your data is secure and private. We only analyze publicly available information with your consent.</p>
        </div>
      </section>

      <section className="how-it-works">
        <h2 style={{ color: '#000' }}>How It Works</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3 style={{ color: '#000' }}>Connect Your Accounts</h3>
            <p style={{ color: '#000' }}>Link your social media profiles securely (Instagram, Twitter, LinkedIn, Reddit)</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3 style={{ color: '#000' }}>AI Analysis</h3>
            <p style={{ color: '#000' }}>Our AI analyzes your digital footprint to understand your personality traits</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3 style={{ color: '#000' }}>Get Insights</h3>
            <p style={{ color: '#000' }}>Receive your detailed personality profile using the Big Five model</p>
          </div>
          <div className="step">
            <div className="step-number">4</div>
            <h3 style={{ color: '#000' }}>Discover & Connect</h3>
            <p style={{ color: '#000' }}>Find relevant events, hackathons, and networking opportunities</p>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <h2 style={{ color: '#000' }}>Ready to Discover Your Digital Self?</h2>
        <p style={{ color: '#000' }}>Join thousands of users who have unlocked their personality insights</p>
        <Link to="/signup" className="btn btn-primary btn-large" style={{ color: '#ff9966' }}>Start Your Journey</Link>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4 style={{ color: '#000' }}>PersonaPulse</h4>
            <p style={{ color: '#000' }}>Discover your digital personality through AI-powered analysis</p>
          </div>
          <div className="footer-section">
            <h4 style={{ color: '#000' }}>Features</h4>
            <ul>
              <li style={{ color: '#000' }}>Personality Analysis</li>
              <li style={{ color: '#000' }}>Event Recommendations</li>
              <li style={{ color: '#000' }}>Networking Opportunities</li>
              <li style={{ color: '#000' }}>Privacy Protection</li>
            </ul>
          </div>
          <div className="footer-section">
            <h4 style={{ color: '#000' }}>Support</h4>
            <ul>
              <li style={{ color: '#000' }}>Help Center</li>
              <li style={{ color: '#000' }}>Privacy Policy</li>
              <li style={{ color: '#000' }}>Terms of Service</li>
              <li style={{ color: '#000' }}>Contact Us</li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p style={{ color: '#000' }}>&copy; 2024 PersonaPulse. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;