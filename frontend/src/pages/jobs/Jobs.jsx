import { useState } from 'react'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'

import { useApi } from '../../hooks/useApi'
import { deleteJob, listJobs } from '../../services/jobService'
import { getErrorMessage } from '../../services/api'
import { LoadingState } from '../../components/common/EmptyState.jsx'
import ConfirmDialog from '../../components/common/ConfirmDialog.jsx'
import StatusBadge from '../../components/common/StatusBadge.jsx'
import { JOB_STATUS_COLORS } from '../../utils/constants'
import { titleCase } from '../../utils/formatters'

export default function Jobs() {
  const { data: jobs, loading, refetch } = useApi(listJobs)
  const [deleteTarget, setDeleteTarget] = useState(null)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Jobs</h1>
          <p className="text-sm text-slate-500">Manage job postings and application links</p>
        </div>
        <div className="flex gap-2">
          <button className="btn-secondary" onClick={() => refetch()}>
            ↻ Refresh
          </button>
          <Link to="/dashboard/jobs/new" className="btn-primary">
            + New Job
          </Link>
        </div>
      </div>

      {loading ? (
        <LoadingState />
      ) : !jobs || jobs.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center">
          <div className="text-4xl">📋</div>
          <h3 className="mt-4 text-lg font-semibold text-slate-800">No jobs yet</h3>
          <p className="mt-1 max-w-sm text-sm text-slate-500">
            Create your first job posting, publish it, and share the public application link with candidates.
          </p>
          <Link to="/dashboard/jobs/new" className="btn-primary mt-5">
            Create a job
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {jobs.map((job) => (
            <div key={job.id} className="card transition hover:border-indigo-300 hover:shadow-md">
              <Link to={`/dashboard/jobs/${job.id}`} className="block">
                <div className="flex items-start justify-between gap-3">
                  <h2 className="font-semibold text-slate-800">{job.title}</h2>
                  <StatusBadge status={job.status} colorMap={JOB_STATUS_COLORS} />
                </div>
                <p className="mt-1 text-sm text-slate-500">
                  {job.location} · {titleCase(job.employment_type)}
                </p>
                <div className="mt-4 flex gap-6 text-sm">
                  <span className="text-slate-600">
                    <span className="font-bold">{job.applications_count ?? 0}</span> applications
                  </span>
                  <span className="text-slate-600">
                    <span className="font-bold text-green-600">{job.shortlisted_count ?? 0}</span> shortlisted
                  </span>
                  {job.average_score !== null && job.average_score !== undefined && (
                    <span className="text-slate-600">avg score {Number(job.average_score).toFixed(1)}</span>
                  )}
                </div>
              </Link>
              <div className="mt-4 flex justify-end gap-2 border-t border-slate-100 pt-3">
                <Link to={`/dashboard/jobs/${job.id}/edit`} className="btn-secondary text-xs" onClick={(e) => e.stopPropagation()}>
                  Edit
                </Link>
                <button
                  className="rounded-lg border border-red-200 bg-white px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50"
                  onClick={() => setDeleteTarget(job)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      <ConfirmDialog
        open={!!deleteTarget}
        title={`Delete "${deleteTarget?.title}"?`}
        message="This will permanently delete the job and all its applications and scores. This cannot be undone."
        confirmLabel="Delete Job"
        onCancel={() => setDeleteTarget(null)}
        onConfirm={async () => {
          try {
            await deleteJob(deleteTarget.id)
            toast.success('Job deleted')
            setDeleteTarget(null)
            refetch()
          } catch (e) {
            toast.error(getErrorMessage(e, 'Could not delete job'))
          }
        }}
      />
    </div>
  )
}
