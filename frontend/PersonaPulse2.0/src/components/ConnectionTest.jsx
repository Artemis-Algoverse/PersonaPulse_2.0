import React, { useState, useEffect } from 'react';
import { CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { personaPulseAPI } from '../services/api';

const ConnectionTest = () => {
  const [status, setStatus] = useState('testing');
  const [message, setMessage] = useState('');

  useEffect(() => {
    testConnection();
  }, []);

  const testConnection = async () => {
    try {
      setStatus('testing');
      setMessage('Testing backend connection...');
      
      const response = await personaPulseAPI.healthCheck();
      
      if (response) {
        setStatus('success');
        setMessage('Backend connection successful!');
      }
    } catch (error) {
      setStatus('error');
      setMessage(`Connection failed: ${error.message}`);
    }
  };

  return (
    <div className="fixed top-20 right-4 z-50 bg-white border border-border rounded-lg shadow-lg p-4 max-w-sm">
      <div className="flex items-center space-x-2">
        {status === 'testing' && <Loader className="h-4 w-4 animate-spin text-blue-500" />}
        {status === 'success' && <CheckCircle className="h-4 w-4 text-green-500" />}
        {status === 'error' && <AlertCircle className="h-4 w-4 text-red-500" />}
        
        <div className="text-sm">
          <div className="font-medium">Backend Status</div>
          <div className={`text-xs ${
            status === 'success' ? 'text-green-600' : 
            status === 'error' ? 'text-red-600' : 'text-blue-600'
          }`}>
            {message}
          </div>
        </div>
      </div>
      
      {status === 'error' && (
        <button
          onClick={testConnection}
          className="mt-2 text-xs bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
        >
          Retry
        </button>
      )}
    </div>
  );
};

export default ConnectionTest;
