import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

import JobForm from '../../components/jobs/JobForm.jsx'
import { createJob } from '../../services/jobService'
import { getErrorMessage } from '../../services/api'

export default function CreateJob() {
  const navigate = useNavigate()
  const [submitting, setSubmitting] = useState(false)

  const onSubmit = async (data) => {
    setSubmitting(true)
    try {
      const job = await createJob({
        ...data,
        required_skills: data.required_skills.split(',').map((s) => s.trim()).filter(Boolean),
        preferred_skills: (data.preferred_skills || '').split(',').map((s) => s.trim()).filter(Boolean),
        minimum_experience: Number(data.minimum_experience) || 0,
      })
      toast.success('Job created as draft. Publish it to generate the application link.')
      navigate(`/dashboard/jobs/${job.id}`)
    } catch (error) {
      toast.error(getErrorMessage(error, 'Could not create job'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Create Job</h1>
        <p className="text-sm text-slate-500">Define the role so the AI can rank candidates accurately</p>
      </div>
      <JobForm onSubmit={onSubmit} submitting={submitting} submitLabel="Create Job" />
    </div>
  )
}
