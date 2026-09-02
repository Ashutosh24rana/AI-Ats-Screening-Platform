export function formatDate(value) {
  if (!value) return '-'
  return new Date(value).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function formatScore(score) {
  if (score === null || score === undefined) return '-'
  return Number(score).toFixed(1)
}

export function scoreColor(score) {
  if (score === null || score === undefined) return 'text-slate-400'
  if (score >= 75) return 'text-green-600'
  if (score >= 60) return 'text-amber-600'
  return 'text-red-600'
}

export function titleCase(value) {
  if (!value) return ''
  const map = { FULL_TIME: 'Full Time', PART_TIME: 'Part Time', CONTRACT: 'Contract', INTERNSHIP: 'Internship' }
  return map[value] || value.charAt(0).toUpperCase() + value.slice(1).toLowerCase().replace('_', ' ')
}
