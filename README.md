# PersonaPulse 2.0

**Discover Your Digital Personality Through AI-Powered Social Media Analysis**

PersonaPulse is a comprehensive platform that analyzes your social media presence across multiple platforms to create a detailed personality profile using advanced AI and the OCEAN personality model.

## 🎯 Features

- **Multi-Platform Analysis**: Instagram, Twitter, LinkedIn, and Reddit
- **AI-Powered Insights**: Uses Google Gemini 2.0 Flash for personality analysis
- **OCEAN Personality Model**: Scientific personality trait assessment
- **Interest Keywords**: Automatic extraction of user interests
- **Beautiful Web Interface**: Modern React frontend with intuitive design
- **Real-time Processing**: Live updates during analysis
- **Automated Updates**: Daily data refresh for evolving personalities
- **Comprehensive API**: RESTful backend for integration

## 🏗️ Architecture

```
PersonaPulse 2.0 Architecture:

[React Frontend] ←→ [Flask API Backend] ←→ [Database]
                           ↓
                  [Social Media Scrapers]
                           ↓
                    [AI Personality Analyzer]
                           ↓
                  [Scheduled Data Updates]
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (with pip)
- Node.js 16+ (with npm)
- Google Gemini API Key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))
- SQLite database (included with Python)

### Manual Setup

1. **Clone Repository:**
   ```bash
   git clone https://github.com/Artemis-Algoverse/PersonaPulse_2.0.git
   cd PersonaPulse_2.0
   ```

2. **Setup Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Copy and configure environment variables
   copy .env.example .env
   # Edit .env and add your Gemini API key from https://makersuite.google.com/app/apikey
   # Start the backend server
   python app.py
   ```

3. **Setup Frontend:**
   ```bash
   cd frontend/PersonaPulse2.0
   npm install
   npm install axios lucide-react
   npm run dev
   ```

4. **Access Application:**
   Open `http://localhost:5173` in your browser

## 🖥️ Usage

1. **Enter Social Media IDs:**
   - Fill in the form with your usernames/profiles
   - At least one platform is required

2. **Start Analysis:**
   - Click "Start Analysis" button
   - Watch real-time progress updates

3. **View Results:**
   - OCEAN personality trait scores (0-100)
   - Interest keywords visualization
   - Platform analysis status
   - Confidence score for analysis

## 📊 Example Results

```json
{
  "interest_keywords": ["technology", "sports", "music", "travel"],
  "ocean_scores": {
    "openness": 75,
    "conscientiousness": 65,
    "extraversion": 80,
    "agreeableness": 70,
    "neuroticism": 30
  },
  "confidence_score": 85
}
```

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core language
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database (file-based, no setup required)
- **Google Gemini 2.0 Flash** - AI analysis
- **APScheduler** - Task scheduling

### Social Media Integration
- **Instaloader** - Instagram public data scraping
- **Web Scraping** - Twitter and Reddit public data (no API keys needed)
- **BeautifulSoup** - LinkedIn public profile scraping

### Frontend
- **React 19** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **Lucide React** - Icons
- **CSS3** - Custom styling

## 📁 Project Structure

```
PersonaPulse_2.0/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── models.py              # Database models
│   ├── services.py            # Business logic
│   ├── ai_analyzer.py         # Gemini AI integration
│   ├── scheduler.py           # Automated updates
│   ├── scrapers/              # Social media scrapers
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend documentation
├── frontend/
│   └── PersonaPulse2.0/
│       ├── src/
│       │   ├── App.jsx        # Main React component
│       │   ├── App.css        # Application styles
│       │   └── index.css      # Global styles
│       ├── package.json       # Node dependencies
│       └── README.md          # Frontend documentation
└── README.md                  # This file
```

## 🔧 Configuration

### Required API Keys

1. **Google Gemini API Only**: Get from [Google AI Studio](https://aistudio.google.com/)

**Note**: No social media API keys required! All platforms use public data scraping with usernames provided through the web form.

### Environment Variables

Edit `backend/.env`:
```bash
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key

# Database (SQLite - no configuration needed)
DATABASE_URL=sqlite:///personapulse.db
```

**Note**: Users provide their social media usernames through the web form - no personal credentials needed in environment variables!

## 🔮 Future Enhancements

- **Event Recommendation System**: Suggest events based on personality
- **Historical Analysis**: Track personality changes over time
- **Social Comparison**: Compare with friends or demographics
- **Advanced Visualizations**: Interactive personality charts
- **Mobile App**: Native mobile applications
- **Privacy Controls**: Enhanced data protection options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational and research purposes. Please ensure compliance with social media platform terms of service.

## 🆘 Support

For issues and questions:
1. Check the documentation in `backend/README.md` and `frontend/README.md`
2. Review the setup scripts and error messages
3. Ensure all API keys are correctly configured
4. Verify that both backend and frontend are running

## 🎉 Acknowledgments

- Google Gemini for AI personality analysis
- Social media platforms for data access
- Open source community for libraries and tools
- OCEAN personality model researchers

---

**PersonaPulse 2.0** - Where your digital footprint reveals your true personality! 🧠✨