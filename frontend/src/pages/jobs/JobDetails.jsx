import { useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import toast from 'react-hot-toast'

import { LoadingState } from '../../components/common/EmptyState.jsx'
import StatusBadge from '../../components/common/StatusBadge.jsx'
import ScoreIndicator from '../../components/common/ScoreIndicator.jsx'
import ConfirmDialog from '../../components/common/ConfirmDialog.jsx'
import { getErrorMessage } from '../../services/api'
import { changeJobStatus, deleteJob, getJobApplications } from '../../services/jobService'
import { useApi } from '../../hooks/useApi'
import { JOB_STATUS_COLORS, PROCESSING_STATUS_COLORS } from '../../utils/constants'
import { formatDate, scoreColor, titleCase } from '../../utils/formatters'

const FILTERS = ['ALL', 'SHORTLISTED', 'REVIEW', 'REJECTED']

export default function JobDetails() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const { data, loading, refetch } = useApi(() => getJobApplications(jobId), [jobId])
  const [filter, setFilter] = useState('ALL')
  const [confirmClose, setConfirmClose] = useState(false)
  const [confirmDelete, setConfirmDelete] = useState(false)

  const job = data?.job
  const counts = data?.counts || { total: 0, shortlisted: 0, review: 0, rejected: 0 }

  const candidates = useMemo(() => {
    const items = data?.candidates || []
    if (filter === 'ALL') return items
    return items.filter((c) => c.status === filter)
  }, [data, filter])

  if (loading) return <LoadingState />
  if (!job) {
    return <p className="text-sm text-red-600">Job not found.</p>
  }

  const applicationUrl = `${window.location.origin}/apply/${job.application_slug}`

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(applicationUrl)
      toast.success('Application link copied!')
    } catch {
      toast.error('Could not copy the link')
    }
  }

  const handleStatusChange = async (status) => {
    try {
      await changeJobStatus(job.id, status)
      toast.success(`Job ${status.toLowerCase()}`)
      setConfirmClose(false)
      refetch()
    } catch (error) {
      toast.error(getErrorMessage(error, 'Could not update status'))
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">{job.title}</h1>
          <p className="text-sm text-slate-500">
            {job.location} · {titleCase(job.employment_type)} · Min {job.minimum_experience} yrs
          </p>
        </div>
        <div className="flex gap-2">
          <button className="btn-secondary" onClick={() => navigate(`/dashboard/jobs/${job.id}/edit`)}>
            Edit
          </button>
          <button className="rounded-lg border border-red-200 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50" onClick={() => setConfirmDelete(true)}>
            Delete
          </button>
          {job.status === 'DRAFT' && (
            <button className="btn-primary" onClick={() => handleStatusChange('PUBLISHED')}>
              Publish Job
            </button>
          )}
          {job.status === 'PUBLISHED' && (
            <button className="btn-secondary" onClick={() => setConfirmClose(true)}>
              Close Job
            </button>
          )}
          {job.status === 'CLOSED' && (
            <button className="btn-primary" onClick={() => handleStatusChange('PUBLISHED')}>
              Reopen Job
            </button>
          )}
        </div>
      </div>

      {/* Application link */}
      <div className="card flex flex-wrap items-center justify-between gap-3 border-indigo-200 bg-indigo-50/50">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-indigo-500">Public Application Link</p>
          <p className="truncate text-sm font-medium text-indigo-900">{applicationUrl}</p>
        </div>
        <button className="btn-primary" onClick={copyLink}>
          Copy Link
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="card py-4 text-center">
          <p className="text-2xl font-bold text-slate-800">{counts.total}</p>
          <p className="text-xs text-slate-500">Total Applications</p>
        </div>
        <div className="card py-4 text-center">
          <p className="text-2xl font-bold text-green-600">{counts.shortlisted}</p>
          <p className="text-xs text-slate-500">Shortlisted</p>
        </div>
        <div className="card py-4 text-center">
          <p className="text-2xl font-bold text-amber-600">{counts.review}</p>
          <p className="text-xs text-slate-500">Under Review</p>
        </div>
        <div className="card py-4 text-center">
          <p className="text-2xl font-bold text-red-600">{counts.rejected}</p>
          <p className="text-xs text-slate-500">Rejected</p>
        </div>
      </div>

      {/* Candidate ranking */}
      <div className="card">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-lg font-semibold text-slate-800">Candidate Ranking</h2>
          <div className="flex gap-1 rounded-lg bg-slate-100 p-1">
            {FILTERS.map((f) => (
              <button
                key={f}
                className={`rounded-md px-3 py-1 text-xs font-medium transition ${
                  filter === f ? 'bg-white text-indigo-600 shadow' : 'text-slate-500 hover:text-slate-700'
                }`}
                onClick={() => setFilter(f)}
              >
                {f.charAt(0) + f.slice(1).toLowerCase()}
              </button>
            ))}
          </div>
        </div>

        {candidates.length === 0 ? (
          <div className="py-12 text-center text-sm text-slate-500">
            No applications yet. Share the public link to start receiving candidates.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-slate-200 text-xs uppercase text-slate-400">
                <tr>
                  <th className="py-3 pr-3 font-medium">Rank</th>
                  <th className="px-3 py-3 font-medium">Candidate</th>
                  <th className="px-3 py-3 font-medium">Score</th>
                  <th className="px-3 py-3 font-medium">Skills</th>
                  <th className="px-3 py-3 font-medium">Experience</th>
                  <th className="px-3 py-3 font-medium">Status</th>
                  <th className="px-3 py-3 font-medium">Applied</th>
                  <th className="px-3 py-3" />
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {candidates.map((candidate) => (
                  <tr key={candidate.application_id} className="hover:bg-slate-50">
                    <td className="py-3 pr-3 font-semibold text-slate-400">#{candidate.rank}</td>
                    <td className="px-3 py-3">
                      <Link
                        to={`/dashboard/candidates/${candidate.application_id}`}
                        className="font-medium text-indigo-600 hover:underline"
                      >
                        {candidate.candidate_name}
                      </Link>
                      <div className="mt-0.5">
                        <StatusBadge status={candidate.processing_status} colorMap={PROCESSING_STATUS_COLORS} />
                      </div>
                    </td>
                    <td className={`px-3 py-3 font-bold ${scoreColor(candidate.final_score)}`}>
                      {candidate.final_score !== null ? Number(candidate.final_score).toFixed(1) : '-'}
                    </td>
                    <td className="max-w-[180px] px-3 py-3">
                      <div className="flex flex-wrap gap-1">
                        {(candidate.matched_skills || []).slice(0, 3).map((skill) => (
                          <span key={skill} className="rounded-full bg-green-50 px-2 py-0.5 text-xs text-green-700">
                            {skill}
                          </span>
                        ))}
                        {(candidate.matched_skills || []).length > 3 && (
                          <span className="text-xs text-slate-400">+{candidate.matched_skills.length - 3}</span>
                        )}
                      </div>
                    </td>
                    <td className="px-3 py-3">
                      {candidate.experience_score !== null ? `${candidate.experience_score}/100` : '-'}
                    </td>
                    <td className="px-3 py-3">
                      <StatusBadge status={candidate.status} />
                    </td>
                    <td className="px-3 py-3 text-slate-500">{formatDate(candidate.applied_at)}</td>
                    <td className="px-3 py-3 text-right">
                      <Link
                        to={`/dashboard/candidates/${candidate.application_id}`}
                        className="text-xs font-medium text-indigo-600 hover:underline"
                      >
                        View →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <ConfirmDialog
        open={confirmClose}
        title="Close this job?"
        message="The public application link will stop accepting new submissions."
        confirmLabel="Close Job"
        onCancel={() => setConfirmClose(false)}
        onConfirm={() => handleStatusChange('CLOSED')}
      />
      <ConfirmDialog
        open={confirmDelete}
        title={`Delete "${job.title}"?`}
        message="This will permanently delete the job and all its applications. This cannot be undone."
        confirmLabel="Delete Job"
        onCancel={() => setConfirmDelete(false)}
        onConfirm={async () => {
          try {
            await deleteJob(job.id)
            toast.success('Job deleted')
            navigate('/dashboard/jobs')
          } catch (e) {
            toast.error(getErrorMessage(e, 'Could not delete job'))
          }
        }}
      />
    </div>
  )
}
