import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  // State for extracted keywords
  const [extractedKeywords, setExtractedKeywords] = useState('');

  // Fetch extracted keywords for user
  useEffect(() => {
    async function fetchKeywords() {
      if (user && user.unique_id) {
        try {
          const res = await fetch(`http://localhost:5000/api/users/${user.unique_id}/keywords`);
          const data = await res.json();
          setExtractedKeywords(data.keywords || '');
        } catch (err) {
          setExtractedKeywords('');
        }
      }
    }
    fetchKeywords();
  }, [user]);
  const [activeTab, setActiveTab] = useState('profile');

  // Center everything visually
  // ...existing code...

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

  // Event recommendations fetched from backend
  const [recommendations, setRecommendations] = useState([]);
  const [loadingEvents, setLoadingEvents] = useState(false);
  const [eventError, setEventError] = useState(null);
  // Import API service
  // ...existing code...
  // Fetch recommended events using extracted keywords
  const fetchEvents = async () => {
    if (!extractedKeywords || extractedKeywords.trim() === '') {
      setRecommendations([]);
      setEventError('No keywords extracted from your profile. Please complete personality analysis.');
      return;
    }
    setLoadingEvents(true);
    setEventError(null);
    try {
      const keywords = extractedKeywords;
      const { data } = await import('../services/APIService').then(mod => mod.matchEvents(keywords));
      setRecommendations(data);
    } catch (err) {
      setEventError('Failed to fetch events');
    }
    setLoadingEvents(false);
  };

  useEffect(() => {
    if (activeTab === 'recommendations') {
      fetchEvents();
    }
    // eslint-disable-next-line
  }, [activeTab, extractedKeywords]);

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
      <nav className="dashboard-nav" style={{justifyContent:'center'}}>
        <div className="nav-brand" style={{textAlign:'center', width:'100%'}}>
          <h2>PersonaPulse</h2>
        </div>
        <div className="nav-user" style={{textAlign:'center', width:'100%'}}>
          <span>Welcome, {user.name}</span>
          <button onClick={handleLogout} className="btn btn-secondary">Logout</button>
        </div>
      </nav>

      <div className="dashboard-header" style={{textAlign:'center', width:'100%'}}>
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

            <div className="profile-card">
              <h2>Extracted Keywords from Your Profile</h2>
              <div style={{marginTop:'1rem', fontWeight:'bold', color:'#a18cd1'}}>
                {extractedKeywords ? extractedKeywords : 'No keywords found.'}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="recommendations-section">
            <h2>Recommended Events</h2>
            <button className="btn btn-primary" style={{marginBottom:'1rem'}} onClick={fetchEvents}>Refresh</button>
            {loadingEvents && <div>Loading events...</div>}
            {eventError && <div style={{color:'red'}}>{eventError}</div>}
            <div className="recommendations-grid">
              {recommendations.length === 0 && !loadingEvents && !eventError && (
                <div>No events found.</div>
              )}
              {recommendations.map((rec) => (
                <div key={rec.id} className="recommendation-card">
                  <div className="card-header">
                    <h3>{rec.title}</h3>
                  </div>
                  <div className="card-content">
                    <p className="event-description">{rec.description}</p>
                    <p className="event-keywords"><b>Keywords:</b> {rec.keywords}</p>
                  </div>
                  <div className="card-actions">
                    <button className="btn btn-primary">Learn More</button>
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