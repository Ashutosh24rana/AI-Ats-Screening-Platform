import { STATUS_COLORS } from '../../utils/constants'

export default function StatusBadge({ status, colorMap }) {
  const colors = colorMap || STATUS_COLORS
  const classes = colors[status] || 'bg-slate-100 text-slate-700'
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${classes}`}>
      {status?.replace('_', ' ').toLowerCase()}
    </span>
  )
}
