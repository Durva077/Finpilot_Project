
import api from './axiosInstance'

// Fetch categories available to the logged-in user.
// Optional categoryType: 'income' or 'expense'.
export const getCategories = async (categoryType) => {
  const response = await api.get('/api/categories', {
    params: categoryType ? { category_type: categoryType } : {},
  })

  return response.data
}
