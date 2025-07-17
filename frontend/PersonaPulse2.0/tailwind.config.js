/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: 'hsl(270, 70%, 50%)',
        accent: 'hsl(330, 80%, 65%)',
        background: 'hsl(0, 0%, 100%)',
        foreground: 'hsl(222.2, 84%, 4.9%)',
        muted: 'hsl(210, 40%, 96.1%)',
        secondary: 'hsl(210, 40%, 96.1%)',
        border: 'hsl(214.3, 31.8%, 91.4%)',
      },
      animation: {
        'fadeIn': 'fadeIn 0.6s ease-in-out',
        'fadeInDelay': 'fadeIn 0.8s ease-in-out 0.2s both',
        'fadeInDelay2': 'fadeIn 1s ease-in-out 0.4s both',
        'fadeInDelay3': 'fadeIn 1.2s ease-in-out 0.6s both',
        'bounce-subtle': 'bounce-subtle 2s infinite',
        'float': 'float 3s ease-in-out infinite',
        'float-delayed': 'float 3s ease-in-out 1.5s infinite',
        'pulse-custom': 'pulse-custom 2s infinite',
        'gradient-x': 'gradient-x 15s ease infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'bounce-subtle': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'pulse-custom': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        'gradient-x': {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
