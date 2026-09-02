import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import toast from 'react-hot-toast'

import JobForm from '../../components/jobs/JobForm.jsx'
import { LoadingState } from '../../components/common/EmptyState.jsx'
import { getErrorMessage } from '../../services/api'
import { getJob, updateJob } from '../../services/jobService'
import { useApi } from '../../hooks/useApi'

export default function EditJob() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const [submitting, setSubmitting] = useState(false)
  const { data: job, loading } = useApi(() => getJob(jobId), [jobId])

  const onSubmit = async (data) => {
    setSubmitting(true)
    try {
      await updateJob(jobId, {
        ...data,
        required_skills: data.required_skills.split(',').map((s) => s.trim()).filter(Boolean),
        preferred_skills: (data.preferred_skills || '').split(',').map((s) => s.trim()).filter(Boolean),
        minimum_experience: Number(data.minimum_experience) || 0,
      })
      toast.success('Job updated')
      navigate(`/dashboard/jobs/${jobId}`)
    } catch (error) {
      toast.error(getErrorMessage(error, 'Could not update job'))
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <LoadingState />

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Edit Job</h1>
        <p className="text-sm text-slate-500">{job?.title}</p>
      </div>
      <JobForm
        initialData={{
          ...job,
          required_skills: (job?.required_skills || []).join(', '),
          preferred_skills: (job?.preferred_skills || []).join(', '),
        }}
        onSubmit={onSubmit}
        submitting={submitting}
        submitLabel="Save Changes"
      />
    </div>
  )
}
