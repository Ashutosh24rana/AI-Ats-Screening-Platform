import api from './api'

export async function listJobs() {
  const response = await api.get('/jobs')
  return response.data
}

export async function getJob(jobId) {
  const response = await api.get(`/jobs/${jobId}`)
  return response.data
}

export async function createJob(data) {
  const response = await api.post('/jobs', data)
  return response.data
}

export async function updateJob(jobId, data) {
  const response = await api.patch(`/jobs/${jobId}`, data)
  return response.data
}

export async function changeJobStatus(jobId, status) {
  const response = await api.post(`/jobs/${jobId}/status`, { status })
  return response.data
}

export async function deleteJob(jobId) {
  await api.delete(`/jobs/${jobId}`)
}

export async function getJobApplications(jobId) {
  const response = await api.get(`/jobs/${jobId}/applications`)
  return response.data
}
