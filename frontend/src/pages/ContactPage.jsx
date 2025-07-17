import React from "react";
export default function ContactPage() {
  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-400 text-transparent bg-clip-text">Contact Us</h1>
      <p className="mb-6">Have questions, feedback, or partnership ideas? Reach out to us below!</p>
      <form className="space-y-4">
        <input type="text" placeholder="Your Name" className="w-full p-3 border rounded" />
        <input type="email" placeholder="Your Email" className="w-full p-3 border rounded" />
        <textarea placeholder="Your Message" className="w-full p-3 border rounded h-32" />
        <button type="submit" className="w-full py-3 font-semibold rounded bg-gradient-to-r from-purple-600 to-pink-400 text-white hover:scale-105 transition">Send Message</button>
      </form>
      <p className="mt-6 text-gray-500">Or email us at <a href="mailto:hello@personapulse.com" className="text-purple-600">hello@personapulse.com</a></p>
    </div>
  );
}
