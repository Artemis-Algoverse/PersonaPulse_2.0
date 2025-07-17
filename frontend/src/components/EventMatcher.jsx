import React, { useState } from "react";
import axios from "axios";

export default function EventMatcher() {
  const [interests, setInterests] = useState("");
  const [profileUrl, setProfileUrl] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("/api/match_user", {
        interests,
        profile_url: profileUrl,
      });
      setResults(res.data.matches || []);
    } catch (err) {
      setError("Could not fetch event recommendations.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-400 text-transparent bg-clip-text">Find Events That Match You</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Your interests (e.g. AI, hackathons, music)"
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
          className="w-full p-3 border rounded"
        />
        <input
          type="url"
          placeholder="Profile URL (optional)"
          value={profileUrl}
          onChange={(e) => setProfileUrl(e.target.value)}
          className="w-full p-3 border rounded"
        />
        <button
          type="submit"
          className="w-full py-3 font-semibold rounded bg-gradient-to-r from-purple-600 to-pink-400 text-white hover:scale-105 transition"
        >
          {loading ? "Matching..." : "Get Recommendations"}
        </button>
      </form>
      {error && <div className="mt-4 text-red-500">{error}</div>}
      <div className="mt-6">
        {results.length > 0 && (
          <div>
            <h3 className="text-xl font-semibold mb-2">Recommended Events:</h3>
            <ul className="space-y-2">
              {results.map((event) => (
                <li key={event.event_id} className="p-4 bg-gray-100 rounded shadow hover:bg-gray-200 transition">
                  <span className="font-bold">{event.title}</span>
                  <span className="ml-2 text-sm text-gray-500">(Score: {event.score.toFixed(2)})</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
