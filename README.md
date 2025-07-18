<h1 align="center">PersonaPulse</h1>
<p align="center"><i>Smart event concierge for your lifestyle — discover events you’ll actually care about.</i></p>

<p align="center">
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/Backend-FastAPI-green?style=flat-square&logo=fastapi" />
  </a>
  <a href="https://reactjs.org/">
    <img src="https://img.shields.io/badge/Frontend-React-blue?style=flat-square&logo=react" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.9%2B-yellow?style=flat-square&logo=python" />
  </a>
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat-square&logo=sqlite" />
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" />
  </a>
</p>


**Discover Events That Match Your Pulse**

PersonaPulse is a React-based web application that analyzes your social media profiles and interests to provide personalized event recommendations. It uses AI-powered keyword matching to find events that truly resonate with your lifestyle and preferences.

##  Features

- Smart Integration: Connect Instagram and LinkedIn profiles for personalized recommendations
- Interest Matching: Advanced keyword matching algorithm to find relevant events
- Real-time Discovery: Live event data from multiple platforms
- Dark/Light Mode: Toggle between themes for comfortable viewing
- Responsive Design: Works perfectly on desktop, tablet, and mobile
- Modern UI: Clean, chic, and attractive interface with smooth animations
- Toast Notifications: Real-time feedback for user actions
- Error Handling: Graceful error boundaries and user-friendly error messages

##  Quick Start

### Prerequisites

- **Python 3.8+** for the backend
- **Node.js 16+** and **npm** for the frontend
- Modern web browser

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Artemis-Algoverse/PersonaPulse.git
   cd PersonaPulse
   ```

2. **Start the Backend Server**
   ```bash
   cd backend/event_tracker
   pip install -r requirements.txt
   python events_api.py
   ```
   Backend will be available at: http://localhost:5000

3. **Start the Frontend Application**
   ```bash
   cd frontend/PersonaPulse
   npm install
   npm run dev
   ```
   Frontend will be available at: http://localhost:5174

##  User Flow

### 1. **Landing Page**
- Welcome screen with feature highlights
- "Get Started" button to begin the journey
- Dark/Light mode toggle in top-right corner

### 2. **Authentication**
- Choose between **Sign In** or **Create Account**
- For new users: Fill out profile information including social media handles
- For existing users: Simple username/password login

### 3. **Loading Screen** (New Accounts Only)
- Animated progress indicator showing current task
- Real-time updates on profile analysis:
  - Creating personalized profile
  - Analyzing social media profiles
  - Extracting interests using AI
  - Matching with relevant events
  - Finalizing dashboard

### 4. **Personal Dashboard**
- Welcome message with user statistics
- Display of extracted interests/keywords
- Grid of personalized event recommendations
- Match percentage for each event
- Quick actions to refresh data or logout PersonaPulse</h1>


## Architecture
Frontend (React) <--> FastAPI Backend <--> Web Scrapers + Profile Scrapers
                                       <--> SQLite DB (Events + Recommendations)

## Contributors
- Built with ❤️ by Artemis @ Algoverse 2025







