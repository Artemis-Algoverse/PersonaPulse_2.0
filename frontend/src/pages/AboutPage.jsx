import React from "react";
export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto p-8">
      <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-400 text-transparent bg-clip-text">About PersonaPulse</h1>
      <p className="text-lg mb-6">PersonaPulse is an AI-powered event recommendation platform that analyzes your social media presence and personality to suggest perfectly matched events. Our mission is to help you discover experiences that truly resonate with who you are.</p>
      <ul className="list-disc pl-6 mb-6">
        <li>AI-driven personality and interest analysis</li>
        <li>Smart event matching using NLP and keyword similarity</li>
        <li>Curated dashboard for personalized recommendations</li>
        <li>Seamless integration with your favorite social platforms</li>
      </ul>
      <p className="text-md text-gray-600">Made with <span className="text-pink-400">❤️</span> by Artemis</p>
    </div>
  );
}
