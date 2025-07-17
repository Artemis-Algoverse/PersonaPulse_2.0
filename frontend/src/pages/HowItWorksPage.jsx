import React from "react";
export default function HowItWorksPage() {
  return (
    <div className="max-w-3xl mx-auto p-8">
      <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-400 text-transparent bg-clip-text">How PersonaPulse Works</h1>
      <ol className="list-decimal pl-6 mb-6 space-y-2">
        <li>Enter your interests or link your public profile.</li>
        <li>Our AI analyzes your personality and social presence.</li>
        <li>We match you to trending and relevant events using smart algorithms.</li>
        <li>View your personalized dashboard and explore events.</li>
      </ol>
      <p className="text-md text-gray-600">Fast, private, and tailored to you.</p>
    </div>
  );
}
