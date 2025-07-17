import React from "react";
import EventMatcher from "../components/EventMatcher";
export default function DashboardPage() {
  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-400 text-transparent bg-clip-text">Your Event Dashboard</h1>
      <p className="mb-6">Enter your interests or profile link to get personalized event recommendations.</p>
      <EventMatcher />
    </div>
  );
}
