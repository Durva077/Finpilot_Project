
import api from './axiosInstance'

export const getDashboardSummary = async () => {
  const response = await api.get('/api/dashboard/summary')
  return response.data
}
