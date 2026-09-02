import api from './api'

export async function getDashboardStats() {
  const response = await api.get('/candidates/dashboard-stats')
  return response.data
}

export async function getMyCompany() {
  const response = await api.get('/companies/me')
  return response.data
}

export async function updateMyCompany(data) {
  const response = await api.patch('/companies/me', data)
  return response.data
}
