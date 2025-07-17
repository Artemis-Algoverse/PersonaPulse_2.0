import React, { useState } from "react";
export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  return (
    <div className="max-w-md mx-auto p-8">
      <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-400 text-transparent bg-clip-text">Login</h1>
      <form className="space-y-4">
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="w-full p-3 border rounded" />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} className="w-full p-3 border rounded" />
        <button type="submit" className="w-full py-3 font-semibold rounded bg-gradient-to-r from-purple-600 to-pink-400 text-white hover:scale-105 transition">Login</button>
      </form>
      <p className="mt-6 text-gray-500">Don't have an account? <a href="/" className="text-purple-600">Sign up</a></p>
    </div>
  );
}
