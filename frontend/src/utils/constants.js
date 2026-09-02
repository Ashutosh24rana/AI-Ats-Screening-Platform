export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const STATUS_COLORS = {
  PENDING: 'bg-slate-100 text-slate-700',
  SCREENING: 'bg-blue-100 text-blue-700',
  SHORTLISTED: 'bg-green-100 text-green-700',
  REVIEW: 'bg-amber-100 text-amber-700',
  REJECTED: 'bg-red-100 text-red-700',
}

export const PROCESSING_STATUS_COLORS = {
  PROCESSING: 'bg-blue-100 text-blue-700',
  COMPLETED: 'bg-green-100 text-green-700',
  FAILED: 'bg-red-100 text-red-700',
}

export const JOB_STATUS_COLORS = {
  DRAFT: 'bg-slate-100 text-slate-700',
  PUBLISHED: 'bg-green-100 text-green-700',
  CLOSED: 'bg-red-100 text-red-700',
}

export const EMPLOYMENT_TYPES = [
  { value: 'FULL_TIME', label: 'Full Time' },
  { value: 'PART_TIME', label: 'Part Time' },
  { value: 'CONTRACT', label: 'Contract' },
  { value: 'INTERNSHIP', label: 'Internship' },
]

export const APPLICATION_STATUSES = ['PENDING', 'SCREENING', 'SHORTLISTED', 'REVIEW', 'REJECTED']

export const SCORE_WEIGHTS = {
  skill: 40,
  experience: 25,
  semantic: 20,
  ats: 15,
}
