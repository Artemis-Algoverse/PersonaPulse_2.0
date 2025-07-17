import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoadingPage = () => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [currentMessage, setCurrentMessage] = useState('');
  const navigate = useNavigate();
  const { user } = useAuth();

  const steps = [
    { 
      text: 'Connecting to social media accounts...', 
      duration: 2000,
      details: 'Establishing secure connections to your profiles'
    },
    { 
      text: 'Analyzing your digital footprint...', 
      duration: 3000,
      details: 'Processing posts, interactions, and engagement patterns'
    },
    { 
      text: 'Processing personality traits...', 
      duration: 2500,
      details: 'Applying Big Five personality model analysis'
    },
    { 
      text: 'Generating recommendations...', 
      duration: 2000,
      details: 'Finding events and connections that match your profile'
    }
  ];

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    const totalDuration = steps.reduce((sum, step) => sum + step.duration, 0);
    let elapsed = 0;
    
    const interval = setInterval(() => {
      elapsed += 100;
      const newProgress = (elapsed / totalDuration) * 100;
      setProgress(Math.min(newProgress, 100));
      
      // Update current step
      let stepElapsed = 0;
      for (let i = 0; i < steps.length; i++) {
        if (elapsed <= stepElapsed + steps[i].duration) {
          setCurrentStep(i);
          setCurrentMessage(steps[i].details);
          break;
        }
        stepElapsed += steps[i].duration;
      }
      
      if (elapsed >= totalDuration) {
        clearInterval(interval);
        setTimeout(() => navigate('/dashboard'), 500);
      }
    }, 100);

    return () => clearInterval(interval);
  }, [navigate, user]);

  return (
    <div className="loading-page">
      <div className="loading-content">
        <div className="loading-header">
          <h1>Analyzing Your Personality</h1>
          <p>Please wait while we process your data, {user?.name}...</p>
        </div>
        
        <div className="progress-container">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="progress-info">
            <span className="progress-percentage">{Math.round(progress)}% Complete</span>
            <span className="progress-time">
              {Math.round((100 - progress) * 0.1)}s remaining
            </span>
          </div>
        </div>

        <div className="current-message">
          <p>{currentMessage}</p>
        </div>

        <div className="analysis-steps">
          {steps.map((step, index) => (
            <div key={index} className={`step-item ${
              index < currentStep ? 'completed' : 
              index === currentStep ? 'current' : 'pending'
            }`}>
              <div className="step-icon">
                {index < currentStep ? '✓' : 
                 index === currentStep ? '⚡' : index + 1}
              </div>
              <div className="step-content">
                <span className="step-text">{step.text}</span>
                {index === currentStep && (
                  <div className="step-loader">
                    <div className="loader-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="loading-facts">
          <h3>Did you know?</h3>
          <div className="fact-rotation">
            <p>The Big Five personality model is used by psychologists worldwide to understand human behavior</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingPage;