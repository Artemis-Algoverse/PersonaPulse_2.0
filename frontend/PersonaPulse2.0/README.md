# PersonaPulse Frontend

A beautiful, modern React application for PersonaPulse - the digital personality analysis platform.

## Features

- **Single Page Application**: Clean, intuitive interface for social media ID input
- **Real-time Form Validation**: Ensures at least one social media platform is provided
- **Beautiful UI/UX**: Modern gradient design with smooth animations and responsive layout
- **Live Results Display**: Shows personality analysis results immediately after processing
- **OCEAN Personality Visualization**: Interactive charts for personality trait scores
- **Interest Keywords Display**: Visual representation of user interests
- **Platform Status Tracking**: Shows which social media platforms were successfully analyzed
- **Loading States**: Engaging loading animation during data processing
- **Error Handling**: User-friendly error messages and feedback

## Technologies Used

- **React 19.1.0** - Modern React with latest features
- **Vite** - Fast build tool and development server
- **Axios** - HTTP client for API communication
- **Lucide React** - Beautiful, customizable icons
- **CSS3** - Custom styling with gradients, animations, and responsive design

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- PersonaPulse backend running on `http://localhost:5000`

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend/PersonaPulse2.0
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Install additional packages:**
   ```bash
   npm install axios lucide-react
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5173`

### Quick Setup (Windows)
```bash
setup.bat
```

### Quick Setup (Unix/Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```

## Usage

1. **Fill in Social Media IDs:**
   - Instagram: Enter your username (without @)
   - Twitter: Enter your username (without @)
   - LinkedIn: Enter your profile URL or username
   - Reddit: Enter your username (without u/)

2. **Submit for Analysis:**
   - At least one platform is required
   - Click "Start Analysis" to begin processing

3. **View Results:**
   - Real-time progress updates during processing
   - Comprehensive personality analysis display
   - OCEAN trait scores with visual bars
   - Interest keywords as colorful tags
   - Platform-wise analysis status

## API Integration

The frontend integrates with the PersonaPulse backend through REST API:

- **Endpoint**: `POST /api/users`
- **Base URL**: `http://localhost:5000/api`
- **CORS**: Enabled for `localhost:5173` and `localhost:3000`

### Request Format
```json
{
  "instagram": "username",
  "twitter": "username", 
  "linkedin": "profile-url",
  "reddit": "username"
}
```

### Response Format
```json
{
  "message": "User created and processed successfully",
  "data": {
    "unique_persona_pulse_id": "uuid",
    "scraping_results": {
      "instagram": true,
      "twitter": true,
      "reddit": false,
      "linkedin": true
    },
    "personality_analysis": {
      "interest_keywords": ["technology", "sports", ...],
      "ocean_scores": {
        "openness": 75,
        "conscientiousness": 65,
        "extraversion": 80,
        "agreeableness": 70,
        "neuroticism": 30
      },
      "confidence_score": 85
    }
  }
}
```

## File Structure

```
src/
├── App.jsx          # Main application component
├── App.css          # Application styles
├── index.css        # Global styles and CSS variables
├── main.jsx         # React app entry point
└── assets/          # Static assets
```

## Design Features

### Color Scheme
- **Primary Gradient**: Purple to blue (`#667eea` to `#764ba2`)
- **Success Colors**: Green variants for successful operations
- **Error Colors**: Red variants for error states
- **Neutral Colors**: Gray variants for text and backgrounds

### Responsive Design
- **Mobile-first approach**: Optimized for mobile devices
- **Tablet optimization**: Adjusted layouts for medium screens
- **Desktop enhancement**: Full features on large screens

### Animations
- **Loading states**: Spinning animations and pulsing effects
- **Hover effects**: Smooth transitions on interactive elements
- **Form validation**: Real-time feedback animations

## Development Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Configuration

The frontend automatically connects to the backend at `http://localhost:5000`. To change this:

1. Update the `API_BASE_URL` constant in `App.jsx`
2. Ensure CORS is configured in the backend for your domain

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Future Enhancements

- **User Dashboard**: Save and view multiple personality analyses
- **Comparison Tool**: Compare personalities across different time periods
- **Export Features**: Download results as PDF or image
- **Social Sharing**: Share personality insights on social media
- **Dark Mode**: Toggle between light and dark themes
- **Detailed Analytics**: More comprehensive personality breakdowns+ Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
