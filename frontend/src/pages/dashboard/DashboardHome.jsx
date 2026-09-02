import { Link } from 'react-router-dom'

import { getDashboardStats } from '../../services/candidateService'
import { listJobs } from '../../services/jobService'
import { useApi } from '../../hooks/useApi'
import StatCard from '../../components/common/StatCard.jsx'
import EmptyState, { LoadingState } from '../../components/common/EmptyState.jsx'
import StatusBadge from '../../components/common/StatusBadge.jsx'
import { JOB_STATUS_COLORS } from '../../utils/constants'
import { formatScore, scoreColor } from '../../utils/formatters'

export default function DashboardHome() {
  const stats = useApi(getDashboardStats)
  const jobs = useApi(listJobs)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Overview</h1>
        <p className="text-sm text-slate-500">Your hiring pipeline at a glance</p>
      </div>

      {stats.loading ? (
        <LoadingState />
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard label="Total Jobs" value={stats.data?.total_jobs} icon="📋" />
          <StatCard label="Active Jobs" value={stats.data?.active_jobs} icon="🚀" accent="text-green-600" />
          <StatCard label="Applications" value={stats.data?.total_applications} icon="📥" accent="text-blue-600" />
          <StatCard label="Shortlisted" value={stats.data?.shortlisted} icon="⭐" accent="text-amber-500" />
        </div>
      )}

      <div className="card">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-800">Your Jobs</h2>
          <Link to="/dashboard/jobs/new" className="btn-primary">
            + New Job
          </Link>
        </div>

        {jobs.loading ? (
          <LoadingState />
        ) : !jobs.data || jobs.data.length === 0 ? (
          <EmptyState
            icon="📋"
            title="No jobs yet"
            description="Create and publish your first job to start receiving AI-ranked applications."
            action={
              <Link to="/dashboard/jobs/new" className="btn-primary">
                Create your first job
              </Link>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-slate-200 text-xs uppercase text-slate-400">
                <tr>
                  <th className="py-3 pr-4 font-medium">Job Title</th>
                  <th className="px-4 py-3 font-medium">Applications</th>
                  <th className="px-4 py-3 font-medium">Shortlisted</th>
                  <th className="px-4 py-3 font-medium">Avg Score</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {jobs.data.map((job) => (
                  <tr key={job.id} className="hover:bg-slate-50">
                    <td className="py-3 pr-4">
                      <Link to={`/dashboard/jobs/${job.id}`} className="font-medium text-indigo-600 hover:underline">
                        {job.title}
                      </Link>
                    </td>
                    <td className="px-4 py-3">{job.applications_count}</td>
                    <td className="px-4 py-3">{job.shortlisted_count}</td>
                    <td className={`px-4 py-3 font-semibold ${scoreColor(job.average_score)}`}>
                      {formatScore(job.average_score)}
                    </td>
                    <td className="px-4 py-3">
                      <StatusBadge status={job.status} colorMap={JOB_STATUS_COLORS} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
