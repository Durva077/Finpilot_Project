import api from './axiosInstance'

// Fetch transactions with optional filters
export const getTransactions = async (filters = {}) => {
  const response = await api.get('/api/transactions', {
    params: filters,
  })
  return response.data
}

// Create a new transaction
export const createTransaction = async (transactionData) => {
  const response = await api.post('/api/transactions', transactionData)
  return response.data
}

// Update an existing transaction
export const updateTransaction = async (id, transactionData) => {
  const response = await api.put(`/api/transactions/${id}`, transactionData)
  return response.data
}

// Delete a transaction
export const deleteTransaction = async (id) => {
  await api.delete(`/api/transactions/${id}`)
}