// src/api.js
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
});

API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

// Intercepta respostas 401 para tentar renovar token
API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Evita loop infinito
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem('refresh')
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh');
        const response = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh: refreshToken,
        });

        const newAccess = response.data.access;
        localStorage.setItem('access', newAccess);

        // Atualiza o header e repete a requisição original
        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        return axios(originalRequest);
      } catch (err) {
        // Refresh token expirou → forçar logout
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        window.location.href = '/';
      }
    }

    return Promise.reject(error);
  }
);

export default API;
