import { Link } from 'react-router-dom'

import { LoadingState } from '../../components/common/EmptyState.jsx'
import StatusBadge from '../../components/common/StatusBadge.jsx'
import { useApi } from '../../hooks/useApi'
import { listApplications } from '../../services/applicationService'
import { PROCESSING_STATUS_COLORS } from '../../utils/constants'
import { formatDate, scoreColor } from '../../utils/formatters'

export default function Candidates() {
  const { data: applications, loading } = useApi(listApplications)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Candidates</h1>
        <p className="text-sm text-slate-500">Everyone who applied to your jobs</p>
      </div>

      {loading ? (
        <LoadingState />
      ) : !applications || applications.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center">
          <div className="text-4xl">🧑‍💻</div>
          <h3 className="mt-4 text-lg font-semibold text-slate-800">No candidates yet</h3>
          <p className="mt-1 max-w-sm text-sm text-slate-500">
            Publish a job and share its public application link to receive candidate resumes.
          </p>
          <Link to="/dashboard/jobs" className="btn-primary mt-5">
            Go to Jobs
          </Link>
        </div>
      ) : (
        <div className="card overflow-x-auto p-0">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-200 text-xs uppercase text-slate-400">
              <tr>
                <th className="px-6 py-3 font-medium">Candidate</th>
                <th className="px-4 py-3 font-medium">Job</th>
                <th className="px-4 py-3 font-medium">ATS Score</th>
                <th className="px-4 py-3 font-medium">Skill Match</th>
                <th className="px-4 py-3 font-medium">Experience</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Applied</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {(applications || []).map((application) => (
                <tr key={application.id} className="hover:bg-slate-50">
                  <td className="px-6 py-3">
                    <Link
                      to={`/dashboard/candidates/${application.id}`}
                      className="font-medium text-indigo-600 hover:underline"
                    >
                      {application.candidate?.name}
                    </Link>
                    <p className="text-xs text-slate-400">{application.candidate?.email}</p>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{application.job?.title}</td>
                  <td className={`px-4 py-3 font-bold ${scoreColor(application.score?.final_score)}`}>
                    {application.score ? Number(application.score.final_score).toFixed(1) : '-'}
                  </td>
                  <td className="px-4 py-3">{application.score ? `${application.score.skill_score}/100` : '-'}</td>
                  <td className="px-4 py-3">
                    {application.score ? `${application.score.experience_score}/100` : '-'}
                  </td>
                  <td className="px-4 py-3 space-y-1">
                    <StatusBadge status={application.status} />
                    <StatusBadge status={application.processing_status} colorMap={PROCESSING_STATUS_COLORS} />
                  </td>
                  <td className="px-4 py-3 text-slate-500">{formatDate(application.applied_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
