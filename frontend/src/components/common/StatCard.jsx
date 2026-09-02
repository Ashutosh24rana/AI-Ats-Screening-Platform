export default function StatCard({ label, value, icon, accent = 'text-indigo-600' }) {
  return (
    <div className="card flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-slate-500">{label}</p>
        <p className="mt-1 text-3xl font-bold text-slate-800">{value ?? 0}</p>
      </div>
      <div className={`text-3xl ${accent}`}>{icon}</div>
    </div>
  )
}
