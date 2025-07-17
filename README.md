# PersonaPulse 2.0

> **AI-Powered Event Recommendation Platform**

PersonaPulse is an innovative AI-powered platform that analyzes users' social media presence and personality traits to recommend perfectly matched events. Built with React, Flask, and Google's Gemini AI, it provides personalized event discovery through advanced personality analysis.

## 🎯 Features

### Core Functionality
- **Multi-Platform Social Media Analysis**: Supports Instagram, Twitter, LinkedIn, and Reddit
- **OCEAN Personality Analysis**: Comprehensive personality profiling using the Five-Factor Model
- **AI-Powered Recommendations**: Gemini AI analyzes personality traits and interests
- **Real-Time Event Matching**: Intelligent matching of events based on personality and interests
- **Beautiful Modern UI**: Responsive design with smooth animations and gradients

### Technical Features
- **Frontend**: React with Tailwind CSS, Vite, and React Router
- **Backend**: Flask REST API with SQLAlchemy and APScheduler
- **Database**: SQLite for development, easily configurable for production
- **AI Integration**: Google Gemini AI for personality analysis
- **Responsive Design**: Mobile-first approach with dark/light theme support
- **Real-Time Updates**: Automated scheduling for data updates

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Start the backend server**
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend/PersonaPulse2.0
   ```

2. **Install dependencies**
   ```bash
   npm install --legacy-peer-deps
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 📖 Usage

### Getting Started
1. **Visit the Homepage**: Navigate to `http://localhost:5173`
2. **Click "Get Started"**: Launch the personality analysis form
3. **Enter Social Media Details**: Provide at least one social media username
4. **Start Analysis**: The AI will analyze your personality and interests
5. **Get Recommendations**: Receive personalized event suggestions

### API Endpoints

#### User Management
- `POST /api/users` - Create new user profile
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get specific user profile

#### Data Processing
- `POST /api/users/<id>/scrape` - Manually trigger data scraping
- `POST /api/users/<id>/analyze` - Manually trigger personality analysis

#### Scheduler
- `GET /api/scheduler/status` - Get scheduler job status
- `POST /api/scheduler/start` - Start scheduled updates

## 🏗️ Architecture

### Frontend Structure
```
frontend/PersonaPulse2.0/
├── src/
│   ├── components/
│   │   ├── ui/           # Reusable UI components
│   │   ├── Navbar.jsx    # Navigation component
│   │   ├── Footer.jsx    # Footer component
│   │   └── MouseFollower.jsx
│   ├── pages/
│   │   ├── Home.jsx      # Landing page with analysis form
│   │   ├── About.jsx     # About page
│   │   └── Contact.jsx   # Contact page
│   ├── services/
│   │   └── api.js        # API service layer
│   └── lib/
│       └── utils.js      # Utility functions
├── tailwind.config.js    # Tailwind configuration
└── package.json
```

### Backend Structure
```
backend/
├── app.py              # Main Flask application
├── models.py           # Database models
├── services.py         # Business logic layer
├── ai_analyzer.py      # AI personality analysis
├── scheduler.py        # Background job scheduler
├── config.py           # Configuration management
├── scrapers/           # Social media scrapers
│   ├── instagram_scraper.py
│   ├── twitter_scraper.py
│   ├── linkedin_scraper.py
│   └── reddit_scraper.py
└── requirements.txt
```

## 🎨 Design System

### Color Palette
- **Primary**: `hsl(270, 70%, 50%)` - Deep Purple
- **Accent**: `hsl(330, 80%, 65%)` - Bright Pink
- **Background**: `hsl(0, 0%, 100%)` - Pure White
- **Foreground**: `hsl(222.2, 84%, 4.9%)` - Dark Gray

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 400 (Normal), 500 (Medium), 600 (Semibold), 700 (Bold)

### Animations
- Fade-in animations with staggered delays
- Hover scale effects on interactive elements
- Floating background shapes
- Smooth theme transitions

## 🔧 Configuration

### Environment Variables
```env
# Backend (.env)
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=sqlite:///personapulse.db
SECRET_KEY=your_secret_key
```

### Development vs Production
- **Development**: Uses SQLite database, debug mode enabled
- **Production**: Configure PostgreSQL/MySQL, disable debug mode

## 📱 Mobile Support

PersonaPulse is fully responsive and optimized for:
- **Mobile phones** (320px+)
- **Tablets** (768px+)
- **Desktop** (1024px+)

## 🔒 Privacy & Security

- **Data Protection**: All personal data is processed securely
- **No API Keys Required**: Social media data collected through web scraping
- **Local Processing**: Personality analysis happens on your server
- **User Control**: Users can manage their data and preferences

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Artemis Team** - Development and design
- **Google Gemini AI** - Personality analysis capabilities
- **Open Source Community** - Various libraries and tools used

## 📞 Support

For support, questions, or feedback:
- **Email**: support@personapulse.com
- **GitHub Issues**: Submit bug reports and feature requests
- **Documentation**: Check the wiki for detailed guides

---

**Made with ❤️ by Artemis**

*PersonaPulse - Discover Events That Match Your Personality*