import api from './axiosInstance'

// Fetch budgets for a specific month and year
export const getBudgets = async (month, year) => {
  const response = await api.get('/api/budgets', {
    params: { month, year },
  })
  return response.data
}

// Create a new budget
export const createBudget = async (budgetData) => {
  const response = await api.post('/api/budgets', budgetData)
  return response.data
}

// Update an existing budget
export const updateBudget = async (id, budgetData) => {
  const response = await api.put(`/api/budgets/${id}`, budgetData)
  return response.data
}

// Delete a budget
export const deleteBudget = async (id) => {
  await api.delete(`/api/budgets/${id}`)
}