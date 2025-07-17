import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  // Mock personality data - in real app, this would come from API
  const personalityTraits = {
    openness: 75,
    conscientiousness: 68,
    extraversion: 82,
    agreeableness: 71,
    neuroticism: 35
  };

  const traitDescriptions = {
    openness: 'Open to new experiences and creative thinking',
    conscientiousness: 'Organized, responsible, and goal-oriented',
    extraversion: 'Outgoing, energetic, and social',
    agreeableness: 'Cooperative, trusting, and empathetic',
    neuroticism: 'Emotionally stable and resilient'
  };

  const traitInsights = {
    openness: 'You enjoy exploring new ideas and are comfortable with ambiguity. Great for creative and innovative roles.',
    conscientiousness: 'You are reliable and organized. You work well in structured environments and meet deadlines.',
    extraversion: 'You gain energy from social interactions and enjoy being around people. Leadership roles suit you well.',
    agreeableness: 'You value harmony and cooperation. You excel in team environments and collaborative projects.',
    neuroticism: 'You handle stress well and remain calm under pressure. You adapt quickly to changing situations.'
  };

  const recommendations = [
    {
      id: 1,
      title: 'Tech Innovation Summit 2024',
      type: 'Technology Conference',
      match: 92,
      reason: 'Perfect for your high openness and extraversion',
      date: '2024-08-15',
      location: 'San Francisco, CA',
      attendees: 500,
      tags: ['Innovation', 'Technology', 'Networking']
    },
    {
      id: 2,
      title: 'Startup Networking Mixer',
      type: 'Networking Event',
      match: 87,
      reason: 'Great for building professional connections',
      date: '2024-07-22',
      location: 'New York, NY',
      attendees: 200,
      tags: ['Startup', 'Networking', 'Business']
    },
    {
      id: 3,
      title: 'Creative Writing Workshop',
      type: 'Workshop',
      match: 78,
      reason: 'Aligns with your creative and open personality',
      date: '2024-07-30',
      location: 'Online',
      attendees: 50,
      tags: ['Creative', 'Writing', 'Skills']
    }
  ];

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const getPersonalityInsight = () => {
    const dominantTrait = Object.entries(personalityTraits).reduce((max, [trait, score]) => 
      score > max.score ? { trait, score } : max, { trait: '', score: 0 }
    );
    
    return {
      trait: dominantTrait.trait,
      message: `Your dominant trait is ${dominantTrait.trait} (${dominantTrait.score}%). ${traitInsights[dominantTrait.trait]}`
    };
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <div className="nav-brand">
          <h2>PersonaPulse</h2>
        </div>
        <div className="nav-user">
          <span>Welcome, {user.name}</span>
          <button onClick={handleLogout} className="btn btn-secondary">Logout</button>
        </div>
      </nav>

      <div className="dashboard-header">
        <h1>Your Personality Profile</h1>
        <p>Discover insights about yourself and find perfect matches</p>
      </div>

      <div className="dashboard-tabs">
        <button 
          className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          Personality Profile
        </button>
        <button 
          className={`tab-button ${activeTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          Recommendations
        </button>
        <button 
          className={`tab-button ${activeTab === 'insights' ? 'active' : ''}`}
          onClick={() => setActiveTab('insights')}
        >
          Insights
        </button>
      </div>

      <div className="dashboard-content">
        {activeTab === 'profile' && (
          <div className="profile-section">
            <div className="profile-card">
              <h2>Big Five Personality Traits</h2>
              <div className="personality-traits">
                {Object.entries(personalityTraits).map(([trait, score]) => (
                  <div key={trait} className="trait">
                    <div className="trait-info">
                      <h3>{trait.charAt(0).toUpperCase() + trait.slice(1)}</h3>
                      <p>{traitDescriptions[trait]}</p>
                    </div>
                    <div className="trait-score">
                      <div className="trait-bar">
                        <div 
                          className="trait-fill" 
                          style={{ width: `${score}%` }}
                        ></div>
                      </div>
                      <span className="score-value">{score}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="profile-card">
              <h2>Your Social Media Profiles</h2>
              <div className="social-profiles">
                {user.instagram && (
                  <div className="social-item">
                    <span className="social-icon">📷</span>
                    <span>Instagram: {user.instagram}</span>
                  </div>
                )}
                {user.twitter && (
                  <div className="social-item">
                    <span className="social-icon">🐦</span>
                    <span>Twitter: {user.twitter}</span>
                  </div>
                )}
                {user.linkedin && (
                  <div className="social-item">
                    <span className="social-icon">💼</span>
                    <span>LinkedIn: {user.linkedin}</span>
                  </div>
                )}
                {user.reddit && (
                  <div className="social-item">
                    <span className="social-icon">🔴</span>
                    <span>Reddit: {user.reddit}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="recommendations-section">
            <h2>Recommended Events</h2>
            <div className="recommendations-grid">
              {recommendations.map((rec) => (
                <div key={rec.id} className="recommendation-card">
                  <div className="card-header">
                    <h3>{rec.title}</h3>
                    <span className="match-badge">{rec.match}% Match</span>
                  </div>
                  <div className="card-content">
                    <p className="event-type">{rec.type}</p>
                    <p className="event-date">📅 {rec.date}</p>
                    <p className="event-location">📍 {rec.location}</p>
                    <p className="event-attendees">👥 {rec.attendees} attendees</p>
                    <p className="match-reason">{rec.reason}</p>
                    <div className="event-tags">
                      {rec.tags.map((tag, index) => (
                        <span key={index} className="tag">{tag}</span>
                      ))}
                    </div>
                  </div>
                  <div className="card-actions">
                    <button className="btn btn-primary">Learn More</button>
                    <button className="btn btn-secondary">Save</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="insights-section">
            <div className="insight-card">
              <h2>Personality Insights</h2>
              <div className="dominant-trait">
                <h3>Your Dominant Trait</h3>
                <p>{getPersonalityInsight().message}</p>
              </div>
              
              <div className="detailed-insights">
                <h3>Detailed Analysis</h3>
                {Object.entries(traitInsights).map(([trait, insight]) => (
                  <div key={trait} className="insight-item">
                    <h4>{trait.charAt(0).toUpperCase() + trait.slice(1)} ({personalityTraits[trait]}%)</h4>
                    <p>{insight}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;