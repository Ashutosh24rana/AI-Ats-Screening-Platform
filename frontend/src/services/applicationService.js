import api from './api'

export async function listApplications() {
  const response = await api.get('/applications')
  return response.data
}

export async function getApplication(applicationId) {
  const response = await api.get(`/applications/${applicationId}`)
  return response.data
}

export async function changeCandidateStatus(applicationId, status) {
  const response = await api.post(`/applications/${applicationId}/status`, { status })
  return response.data
}

export async function retryProcessing(applicationId) {
  const response = await api.post(`/applications/${applicationId}/retry`)
  return response.data
}

export function resumeDownloadUrl(applicationId) {
  return `/applications/${applicationId}/resume`
}
