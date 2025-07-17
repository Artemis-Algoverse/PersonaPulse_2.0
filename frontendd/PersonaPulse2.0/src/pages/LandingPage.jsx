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
        <h1>Discover Your Digital Personality</h1>
        <p>
          Unlock insights into your personality through AI-powered analysis of your social media presence. 
          Get personalized recommendations for events, connections, and growth opportunities.
        </p>
        <Link to="/signup" className="btn btn-primary btn-large">Get Started</Link>
      </section>

      <section className="features">
        <div className="feature-card">
          <div className="feature-icon">🧠</div>
          <h3>AI-Powered Analysis</h3>
          <p>Advanced algorithms analyze your social media activity to understand your personality traits using the Big Five model.</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🎯</div>
          <h3>Personalized Recommendations</h3>
          <p>Get tailored event suggestions and networking opportunities based on your unique personality profile.</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🔒</div>
          <h3>Privacy First</h3>
          <p>Your data is secure and private. We only analyze publicly available information with your consent.</p>
        </div>
      </section>

      <section className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Connect Your Accounts</h3>
            <p>Link your social media profiles securely (Instagram, Twitter, LinkedIn, Reddit)</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>AI Analysis</h3>
            <p>Our AI analyzes your digital footprint to understand your personality traits</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Get Insights</h3>
            <p>Receive your detailed personality profile using the Big Five model</p>
          </div>
          <div className="step">
            <div className="step-number">4</div>
            <h3>Discover & Connect</h3>
            <p>Find relevant events, hackathons, and networking opportunities</p>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <h2>Ready to Discover Your Digital Self?</h2>
        <p>Join thousands of users who have unlocked their personality insights</p>
        <Link to="/signup" className="btn btn-primary btn-large">Start Your Journey</Link>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>PersonaPulse</h4>
            <p>Discover your digital personality through AI-powered analysis</p>
          </div>
          <div className="footer-section">
            <h4>Features</h4>
            <ul>
              <li>Personality Analysis</li>
              <li>Event Recommendations</li>
              <li>Networking Opportunities</li>
              <li>Privacy Protection</li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Support</h4>
            <ul>
              <li>Help Center</li>
              <li>Privacy Policy</li>
              <li>Terms of Service</li>
              <li>Contact Us</li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2024 PersonaPulse. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;