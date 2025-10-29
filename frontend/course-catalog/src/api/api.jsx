import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'https://ivr-calling-1nyf.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API calls
export const makeCall = async (callData) => {
  try {
    const response = await api.post('/make_call', callData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/healthz');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export default api;