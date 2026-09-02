import axios from 'axios'

import { API_BASE_URL } from '../utils/constants'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('ats_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && window.location.pathname.startsWith('/dashboard')) {
      localStorage.removeItem('ats_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

export function getErrorMessage(error, fallback = 'Something went wrong') {
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((d) => d.msg || d.message).join(', ')
  }
  return fallback
}

export default api
