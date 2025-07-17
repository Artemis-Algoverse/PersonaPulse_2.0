import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('Making request to:', config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const personaPulseAPI = {
  // Create new user profile
  createUser: async (socialMediaIds) => {
    try {
      const response = await api.post('/users', socialMediaIds);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to create user profile');
    }
  },

  // Get all users
  getAllUsers: async () => {
    try {
      const response = await api.get('/users');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get users');
    }
  },

  // Get specific user
  getUser: async (uniqueId) => {
    try {
      const response = await api.get(`/users/${uniqueId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get user');
    }
  },

  // Manual scrape
  scrapeUser: async (uniqueId) => {
    try {
      const response = await api.post(`/users/${uniqueId}/scrape`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to scrape user data');
    }
  },

  // Manual analyze
  analyzeUser: async (uniqueId) => {
    try {
      const response = await api.post(`/users/${uniqueId}/analyze`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to analyze user');
    }
  },

  // Get scheduler status
  getSchedulerStatus: async () => {
    try {
      const response = await api.get('/scheduler/status');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get scheduler status');
    }
  },

  // Start scheduler
  startScheduler: async () => {
    try {
      const response = await api.post('/scheduler/start');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to start scheduler');
    }
  },

  // Get user logs
  getUserLogs: async (uniqueId) => {
    try {
      const response = await api.get(`/logs/${uniqueId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get user logs');
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      throw new Error('Backend is not accessible');
    }
  },
};

export default api;
