export default function PipelinePreview() {
  return (
    <div className="relative mx-auto max-w-[640px]">
      {/* glow */}
      <div className="absolute -inset-6 -z-10 rounded-[32px] bg-gradient-to-br from-amber-200 via-orange-200 to-rose-200 opacity-50 blur-2xl" />
      {/* browser chrome */}
      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_20px_60px_-20px_rgba(0,0,0,0.2)]">
        <div className="flex items-center gap-1.5 border-b border-slate-100 bg-slate-50 px-4 py-2.5">
          <span className="h-2.5 w-2.5 rounded-full bg-red-400" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-400" />
          <span className="h-2.5 w-2.5 rounded-full bg-green-400" />
          <span className="ml-3 rounded-full bg-white px-3 py-1 text-xs font-medium text-slate-500 ring-1 ring-slate-200">talent.ai / jobs / senior-backend</span>
          <span className="ml-auto flex items-center gap-1 text-xs font-medium text-emerald-600">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-500" /> Live
          </span>
        </div>
        <div className="grid grid-cols-[1.1fr_0.9fr] gap-4 p-4 sm:p-5">
          {/* left: job */}
          <div className="space-y-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-indigo-500">Public application link</p>
              <p className="mt-1 truncate rounded-lg bg-indigo-50 px-2.5 py-1.5 font-mono text-xs text-indigo-700 ring-1 ring-indigo-100">/apply/7f83a92 · Copy</p>
            </div>
            <div className="grid grid-cols-3 gap-2">
              {[
                { k: 'Total', v: '24' },
                { k: 'Shortlisted', v: '7', c: 'text-emerald-600' },
                { k: 'Avg score', v: '81.4' },
              ].map((s) => (
                <div key={s.k} className="rounded-xl border border-slate-100 bg-slate-50 px-2 py-2 text-center">
                  <p className={`text-lg font-bold ${s.c || 'text-slate-900'}`}>{s.v}</p>
                  <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">{s.k}</p>
                </div>
              ))}
            </div>
            <div className="rounded-xl border border-slate-200 p-3">
              <p className="text-xs font-semibold text-slate-900">Top match · 94.2 — Strong Match</p>
              <div className="mt-2 flex flex-wrap gap-1">
                {['Python', 'FastAPI', 'PostgreSQL', 'Docker'].map((t) => (
                  <span key={t} className="rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-700 ring-1 ring-emerald-100">
                    {t}
                  </span>
                ))}
              </div>
              <p className="mt-2 text-xs leading-relaxed text-slate-500">“Strong backend API experience, relevant FastAPI projects, exceeds 3y requirement.”</p>
            </div>
          </div>
          {/* right: pipeline */}
          <div className="rounded-xl bg-slate-900 p-3 text-white">
            <p className="text-xs font-semibold tracking-wide text-slate-400">PIPELINE</p>
            <div className="mt-3 space-y-2.5">
              {[
                { label: 'PDF → text & chunks', done: true },
                { label: 'Gemini embeddings → Pinecone', done: true },
                { label: 'RAG retrieval (job-aware)', done: true },
                { label: 'LangGraph · 5 evaluations', active: true },
                { label: 'Weighted score & decision', pending: true },
              ].map((r) => (
                <div key={r.label} className="flex items-center gap-2">
                  <span
                    className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px] ${
                      r.done ? 'bg-emerald-500 text-white' : r.active ? 'animate-pulse bg-indigo-500 text-white' : 'bg-white/10 text-white/40 ring-1 ring-white/10'
                    }`}
                  >
                    {r.done ? '✓' : r.active ? '●' : '○'}
                  </span>
                  <span className={`text-xs ${r.active ? 'font-semibold text-white' : r.done ? 'text-white/90' : 'text-white/40'}`}>{r.label}</span>
                </div>
              ))}
            </div>
            <div className="mt-4 grid grid-cols-4 gap-1.5">
              {[
                { l: 'Skill', v: '75', w: '40%' },
                { l: 'Exp', v: '85', w: '25%' },
                { l: 'Sem', v: '95', w: '20%' },
                { l: 'ATS', v: '92', w: '15%' },
              ].map((m) => (
                <div key={m.l} className="rounded-lg bg-white/10 px-1.5 py-2 text-center ring-1 ring-white/10">
                  <p className="text-sm font-bold">{m.v}</p>
                  <p className="text-[10px] uppercase tracking-wide text-white/50">{m.l}</p>
                  <p className="text-[10px] text-white/30">{m.w}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
