import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import toast from 'react-hot-toast'

import { LoadingState } from '../../components/common/EmptyState.jsx'
import StatusBadge from '../../components/common/StatusBadge.jsx'
import ScoreIndicator from '../../components/common/ScoreIndicator.jsx'
import ConfirmDialog from '../../components/common/ConfirmDialog.jsx'
import { useApi } from '../../hooks/useApi'
import { getErrorMessage } from '../../services/api'
import { changeCandidateStatus, getApplication, resumeDownloadUrl } from '../../services/applicationService'
import { APPLICATION_STATUSES, PROCESSING_STATUS_COLORS } from '../../utils/constants'
import { formatDate, scoreColor, titleCase } from '../../utils/formatters'

export default function CandidateDetails() {
  const { applicationId } = useParams()
  const { data: application, loading, refetch } = useApi(() => getApplication(applicationId), [applicationId])
  const [pendingStatus, setPendingStatus] = useState(null)
  const [updating, setUpdating] = useState(false)

  if (loading) return <LoadingState />
  if (!application) {
    return <p className="text-sm text-red-600">Candidate application not found.</p>
  }

  const score = application.score
  const candidate = application.candidate

  const handleStatusChange = async () => {
    setUpdating(true)
    try {
      await changeCandidateStatus(application.id, pendingStatus)
      toast.success(`Status updated to ${pendingStatus}`)
      setPendingStatus(null)
      refetch()
    } catch (error) {
      toast.error(getErrorMessage(error, 'Could not update status'))
    } finally {
      setUpdating(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <Link to="/dashboard/candidates" className="text-xs font-medium text-indigo-600 hover:underline">
            ← All candidates
          </Link>
          <h1 className="mt-1 text-2xl font-bold text-slate-800">{candidate?.name}</h1>
          <p className="text-sm text-slate-500">
            {candidate?.email} · {candidate?.phone || 'No phone'} · Applied {formatDate(application.applied_at)}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select
            className="input-field w-40"
            value={application.status}
            onChange={(e) => setPendingStatus(e.target.value)}
            disabled={updating}
          >
            {APPLICATION_STATUSES.map((status) => (
              <option key={status} value={status}>
                {titleCase(status)}
              </option>
            ))}
          </select>
          {pendingStatus && pendingStatus !== application.status && (
            <button className="btn-primary" onClick={handleStatusChange} disabled={updating}>
              Apply
            </button>
          )}
        </div>
      </div>

      {/* Processing state */}
      <div className="flex flex-wrap items-center gap-3 rounded-xl border border-slate-200 bg-white p-4">
        <StatusBadge status={application.status} />
        <StatusBadge status={application.processing_status} colorMap={PROCESSING_STATUS_COLORS} />
        {application.processing_error && (
          <p className="text-xs text-red-500">Processing error: {application.processing_error}</p>
        )}
        <a
          href={`${resumeDownloadUrl(application.id)}`}
          target="_blank"
          rel="noreferrer"
          className="btn-secondary ml-auto"
          style={{ display: 'inline-flex' }}
        >
          View Resume (PDF)
        </a>
      </div>

      {/* Scores */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="card flex flex-col items-center justify-center">
          <ScoreIndicator score={score?.final_score} size={110} label="Final Score" />
          {score?.recommendation && (
            <span
              className={`mt-3 rounded-full px-3 py-1 text-sm font-semibold ${
                score.recommendation === 'Strong Match'
                  ? 'bg-green-100 text-green-700'
                  : score.recommendation === 'Good Match'
                    ? 'bg-blue-100 text-blue-700'
                    : score.recommendation === 'Moderate Match'
                      ? 'bg-amber-100 text-amber-700'
                      : 'bg-red-100 text-red-700'
              }`}
            >
              {score.recommendation}
            </span>
          )}
        </div>
        <div className="card lg:col-span-2">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Score Breakdown</h2>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            {[
              ['Skill Match', score?.skill_score],
              ['Experience', score?.experience_score],
              ['Semantic Fit', score?.semantic_match_score],
              ['ATS Quality', score?.ats_score],
            ].map(([label, value]) => (
              <div key={label} className="rounded-lg bg-slate-50 p-4 text-center">
                <p className={`text-2xl font-bold ${scoreColor(value)}`}>{value ?? '-'}</p>
                <p className="mt-1 text-xs text-slate-500">{label}</p>
              </div>
            ))}
          </div>
          {!score && (
            <p className="mt-4 text-sm text-slate-500">AI evaluation has not completed yet for this candidate.</p>
          )}
        </div>
      </div>

      {score && (
        <>
          {/* Skills */}
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="card">
              <h3 className="mb-3 font-semibold text-green-700">Matched Skills</h3>
              {score.matched_skills?.length ? (
                <div className="flex flex-wrap gap-2">
                  {score.matched_skills.map((skill) => (
                    <span key={skill} className="rounded-full bg-green-50 px-3 py-1 text-sm text-green-700">
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-400">No matched skills recorded</p>
              )}
            </div>
            <div className="card">
              <h3 className="mb-3 font-semibold text-red-700">Missing Skills</h3>
              {score.missing_skills?.length ? (
                <div className="flex flex-wrap gap-2">
                  {score.missing_skills.map((skill) => (
                    <span key={skill} className="rounded-full bg-red-50 px-3 py-1 text-sm text-red-700">
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-400">None — all required skills matched</p>
              )}
            </div>
          </div>

          {/* Strengths & weaknesses */}
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="card">
              <h3 className="mb-3 font-semibold text-slate-800">Strengths</h3>
              <ul className="space-y-2">
                {(score.strengths || []).map((item, index) => (
                  <li key={index} className="flex gap-2 text-sm text-slate-600">
                    <span className="text-green-600">+</span> {item}
                  </li>
                ))}
                {!score.strengths?.length && <p className="text-sm text-slate-400">None recorded</p>}
              </ul>
            </div>
            <div className="card">
              <h3 className="mb-3 font-semibold text-slate-800">Weaknesses</h3>
              <ul className="space-y-2">
                {(score.weaknesses || []).map((item, index) => (
                  <li key={index} className="flex gap-2 text-sm text-slate-600">
                    <span className="text-red-500">−</span> {item}
                  </li>
                ))}
                {!score.weaknesses?.length && <p className="text-sm text-slate-400">None recorded</p>}
              </ul>
            </div>
          </div>

          {/* AI summary */}
          <div className="card border-indigo-100 bg-indigo-50/40">
            <h3 className="mb-2 font-semibold text-indigo-900">AI Summary</h3>
            <p className="text-sm leading-relaxed text-slate-700">{score.ai_summary || 'No summary generated.'}</p>
          </div>
        </>
      )}

      <ConfirmDialog
        open={!!pendingStatus}
        title={`Change status to ${pendingStatus}?`}
        message="This updates the candidate's stage in your pipeline."
        confirmLabel="Update Status"
        onCancel={() => setPendingStatus(null)}
        onConfirm={handleStatusChange}
      />
    </div>
  )
}
