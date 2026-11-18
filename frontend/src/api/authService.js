
import api from './axiosInstance'

// Register a new user
export const registerUser = async (userData) => {
  const response = await api.post('/api/auth/register', userData)
  return response.data
}

// Login an existing user
export const loginUser = async (credentials) => {
  const response = await api.post('/api/auth/login', credentials)
  return response.data
}
