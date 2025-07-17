import React, { useState, useEffect } from 'react';

const MouseFollower = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div
      className="fixed pointer-events-none z-50 w-4 h-4 bg-gradient-to-r from-primary to-accent rounded-full opacity-50 blur-sm transition-opacity duration-300"
      style={{
        left: mousePosition.x - 8,
        top: mousePosition.y - 8,
        background: 'radial-gradient(circle, hsl(270, 70%, 50%) 0%, hsl(330, 80%, 65%) 100%)',
      }}
    />
  );
};

export default MouseFollower;
