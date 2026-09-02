import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'

import Spinner from '../../components/common/Spinner.jsx'
import api, { getErrorMessage } from '../../services/api'
import { isPdfFile, isWithinSizeLimit } from '../../utils/validators'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function JobApplication() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [job, setJob] = useState(null)
  const [jobError, setJobError] = useState(null)
  const [file, setFile] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm()

  // Load public job details (no auth)
  useEffect(() => {
    fetch(`${API_BASE}/api/v1/public/jobs/${slug}`)
      .then(async (response) => {
        if (!response.ok) {
          const data = await response.json().catch(() => ({}))
          throw new Error(data.detail || 'This application link is invalid')
        }
        return response.json()
      })
      .then(setJob)
      .catch((error) => setJobError(error.message))
  }, [slug])

  const onSubmit = async (data) => {
    if (!file) {
      toast.error('Please attach your resume as a PDF')
      return
    }
    if (!isPdfFile(file)) {
      toast.error('Resume must be a PDF file')
      return
    }
    if (!isWithinSizeLimit(file)) {
      toast.error('Resume must be smaller than 10MB')
      return
    }
    setSubmitting(true)
    try {
      const formData = new FormData()
      formData.append('name', data.name)
      formData.append('email', data.email)
      formData.append('phone', data.phone || '')
      formData.append('resume', file)
      await api.post(`/public/jobs/${slug}/apply`, formData)
      navigate(`/apply/${slug}/success`)
    } catch (error) {
      toast.error(getErrorMessage(error, 'Could not submit application'))
    } finally {
      setSubmitting(false)
    }
  }

  if (jobError) {
    return (
      <div className="flex min-h-screen items-center justify-center px-4">
        <div className="card max-w-md text-center">
          <div className="text-4xl">🔗</div>
          <h1 className="mt-3 text-lg font-semibold text-slate-800">Link unavailable</h1>
          <p className="mt-1 text-sm text-slate-500">{jobError}</p>
        </div>
      </div>
    )
  }

  if (!job) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="mx-auto max-w-2xl space-y-6">
        {/* Job header */}
        <div className="card border-indigo-100 bg-white">
          <p className="text-xs font-semibold uppercase tracking-wide text-indigo-500">{job.company_name}</p>
          <h1 className="mt-1 text-2xl font-bold text-slate-800">{job.title}</h1>
          <p className="mt-1 text-sm text-slate-500">
            {job.location} · Min experience: {job.minimum_experience} years
          </p>

          {(job.required_skills?.length > 0 || job.preferred_skills?.length > 0) && (
            <div className="mt-4 flex flex-wrap gap-2">
              {job.required_skills.map((skill) => (
                <span key={skill} className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-700">
                  {skill}
                </span>
              ))}
              {job.preferred_skills.map((skill) => (
                <span key={skill} className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                  {skill} (nice to have)
                </span>
              ))}
            </div>
          )}

          <p className="mt-4 whitespace-pre-wrap text-sm leading-relaxed text-slate-700">{job.description}</p>
        </div>

        {/* Application form */}
        <form onSubmit={handleSubmit(onSubmit)} className="card space-y-4">
          <h2 className="text-lg font-semibold text-slate-800">Apply for this position</h2>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="label" htmlFor="name">Full name</label>
              <input
                id="name"
                className="input-field"
                placeholder="Jane Doe"
                {...register('name', { required: 'Name is required' })}
              />
              {errors.name && <p className="mt-1 text-xs text-red-600">{errors.name.message}</p>}
            </div>
            <div>
              <label className="label" htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                className="input-field"
                placeholder="jane@example.com"
                {...register('email', { required: 'Email is required' })}
              />
              {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email.message}</p>}
            </div>
          </div>

          <div>
            <label className="label" htmlFor="phone">Phone (optional)</label>
            <input id="phone" className="input-field" placeholder="+1 555 000 0000" {...register('phone')} />
          </div>

          <div>
            <label className="label" htmlFor="resume">Resume (PDF, max 10MB)</label>
            <input
              id="resume"
              type="file"
              accept=".pdf,application/pdf"
              className="input-field file:mr-3 file:rounded-md file:border-0 file:bg-indigo-50 file:px-3 file:py-1.5 file:text-sm file:font-medium file:text-indigo-700"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            {file && <p className="mt-1 text-xs text-slate-500">Selected: {file.name}</p>}
          </div>

          <button type="submit" className="btn-primary w-full" disabled={submitting}>
            {submitting ? 'Submitting...' : 'Submit Application'}
          </button>
          <p className="text-center text-xs text-slate-400">
            Your resume will be analyzed by AI and ranked against this role.
          </p>
        </form>
      </div>
    </div>
  )
}
