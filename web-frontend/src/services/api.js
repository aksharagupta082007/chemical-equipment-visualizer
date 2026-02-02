import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/";

// Helper for requests that pull token directly from storage
const getAuthHeader = () => {
  const token = localStorage.getItem("accessToken");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// Upload CSV - Modified to accept token from component state
export const uploadCSV = (file, token) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post(`${API_URL}upload/`, formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    },
  });
};

// Get history - Modified to accept token from App.js
export const getHistory = (token) => {
  return axios.get(`${API_URL}history/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

// Login to get tokens
export const login = (username, password) => {
  return axios.post(`${API_URL}token/`, { username, password });
};

// Refresh access token
export const refreshToken = (refresh) => {
  return axios.post(`${API_URL}token/refresh/`, { refresh });
};