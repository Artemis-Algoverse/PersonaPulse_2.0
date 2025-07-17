import React from "react";
import { Link } from "react-router-dom";
import { Users, Brain, Target, Sparkles, ArrowRight, Menu } from "lucide-react";
import EventMatcher from "./EventMatcher";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-800">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-600 to-pink-400 flex items-center justify-center">
            <Sparkles className="text-white" size={20} />
          </div>
          <span className="font-bold text-xl bg-gradient-to-r from-purple-600 to-pink-400 text-transparent bg-clip-text">PersonaPulse</span>
        </div>
        <div className="hidden md:flex gap-6 items-center">
          <Link to="/" className="hover:text-purple-600">Home</Link>
          <Link to="/about" className="hover:text-purple-600">About</Link>
          <Link to="/how" className="hover:text-purple-600">How it Works</Link>
          <Link to="/contact" className="hover:text-purple-600">Contact</Link>
          <button className="ml-4 px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-400 text-white font-semibold hover:scale-105 transition">Get Started</button>
        </div>
        <button className="md:hidden p-2 rounded bg-gray-100 dark:bg-gray-800">
          <Menu />
        </button>
      </nav>

      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center py-16 px-4 text-center relative overflow-hidden">
        <h1 className="text-5xl md:text-7xl font-extrabold mb-4 bg-gradient-to-r from-purple-600 to-pink-400 text-transparent bg-clip-text animate-pulse">PersonaPulse</h1>
        <p className="text-xl md:text-2xl mb-8 text-gray-700 dark:text-gray-300">Discover Events That Match Your Personality</p>
        <div className="flex gap-4 mb-8">
          <button className="px-6 py-3 rounded font-semibold bg-gradient-to-r from-purple-600 to-pink-400 text-white hover:scale-105 transition">Get Started</button>
          <button className="px-6 py-3 rounded font-semibold border border-gray-300 dark:border-gray-700 text-purple-600 hover:bg-purple-50 transition">Learn More</button>
        </div>
        {/* Animated floating shapes */}
        <div className="absolute top-0 left-0 w-full h-full pointer-events-none z-0">
          <div className="absolute left-10 top-20 w-24 h-24 rounded-full bg-gradient-to-r from-purple-600 to-pink-400 opacity-30 animate-float" />
          <div className="absolute right-20 bottom-10 w-16 h-16 rounded-full bg-pink-400 opacity-20 animate-float2" />
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-6xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <FeatureCard icon={<Users />} title="Social Analysis" desc="Analyzes your social media presence for event matching." />
        <FeatureCard icon={<Brain />} title="Personality Scoring" desc="OCEAN personality analysis for deeper recommendations." />
        <FeatureCard icon={<Target />} title="Smart Matching" desc="Aligns your interests and personality with event keywords." />
        <FeatureCard icon={<Sparkles />} title="Curated Dashboard" desc="Personalized event recommendations just for you." />
      </section>

      {/* Event Matcher Section */}
      <section className="max-w-3xl mx-auto px-4 py-12">
        <EventMatcher />
      </section>

      {/* Call-to-Action Section */}
      <section className="bg-gradient-to-r from-purple-600 to-pink-400 text-white py-16 text-center">
        <h2 className="text-3xl md:text-5xl font-bold mb-4">Ready to Find Your Perfect Events?</h2>
        <p className="mb-6 text-lg">Start your journey with PersonaPulse and discover events tailored to your personality.</p>
        <button className="px-8 py-4 rounded font-semibold bg-white text-purple-600 hover:scale-105 transition">Start Your Journey</button>
      </section>

      {/* Footer */}
      <footer className="flex items-center justify-between px-6 py-6 border-t border-gray-200 dark:border-gray-800 mt-8">
        <div className="flex items-center gap-2">
          <Sparkles className="text-purple-600" size={20} />
          <span className="font-bold">PersonaPulse</span>
        </div>
        <span className="text-sm text-gray-500">Made with <span className="text-pink-400">❤️</span> by Artemis</span>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, desc }) {
  return (
    <div className="p-6 bg-gray-100 dark:bg-gray-900 rounded-lg shadow-lg flex flex-col items-center text-center hover:scale-105 transition">
      <div className="mb-4 text-purple-600">{icon}</div>
      <h3 className="font-semibold text-lg mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-300">{desc}</p>
    </div>
  );
}
