import { scoreColor } from '../../utils/formatters'

function ring(score) {
  const clamped = Math.max(0, Math.min(100, score ?? 0))
  return `conic-gradient(currentColor ${clamped * 3.6}deg, #e2e8f0 ${clamped * 3.6}deg)`
}

export default function ScoreIndicator({ score, size = 72, label = 'Score' }) {
  return (
    <div className="flex flex-col items-center">
      <div
        className={`relative flex items-center justify-center rounded-full p-1.5 ${scoreColor(score)}`}
        style={{ width: size, height: size, background: ring(score) }}
        aria-label={`${label}: ${score}`}
      >
        <div className="flex h-full w-full items-center justify-center rounded-full bg-white text-sm font-bold">
          {score === null || score === undefined ? '-' : Number(score).toFixed(0)}
        </div>
      </div>
      <span className="mt-1 text-xs text-slate-500">{label}</span>
    </div>
  )
}
