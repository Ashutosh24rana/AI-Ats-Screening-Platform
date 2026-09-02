export default function Features() {
  return (
    <section id="features" className="relative overflow-hidden bg-slate-950 py-16 sm:py-20">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px]" />
        <div className="absolute bottom-0 left-1/2 h-[400px] w-[800px] -translate-x-1/2 rounded-full bg-gradient-to-br from-amber-500/10 via-orange-500/10 to-rose-500/10 blur-3xl" />
      </div>
      <div className="relative mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-xs font-bold uppercase tracking-widest text-amber-300">Why this ATS</p>
          <h2 className="mt-2 text-2xl font-black tracking-tight text-white sm:text-3xl">Built like a real product</h2>
          <p className="mt-2 text-sm text-slate-400">Not a demo — thin routers, Pydantic everywhere, and explainable AI you can trust.</p>
        </div>

        <div className="mt-10 grid gap-4 md:grid-cols-12">
          {/* large */}
          <div className="rounded-2xl border border-amber-400/20 bg-gradient-to-br from-amber-500/10 via-orange-500/5 to-transparent p-6 backdrop-blur md:col-span-7">
            <p className="text-xs font-bold uppercase tracking-widest text-amber-300">Explainable</p>
            <h3 className="mt-1 text-lg font-bold text-white">Every score tells you why</h3>
            <p className="mt-2 max-w-lg text-sm leading-relaxed text-slate-400">
              Matched vs missing skills, strengths & weaknesses, experience vs requirement, and a natural-language summary — all validated by Pydantic structured outputs.
            </p>
            <div className="mt-4 flex flex-wrap gap-1.5">
              {['Skill 40%', 'Experience 25%', 'Semantic 20%', 'ATS 15%'].map((t) => (
                <span key={t} className="rounded-full bg-white px-2.5 py-1 text-xs font-bold text-slate-900 ring-1 ring-white/10">
                  {t}
                </span>
              ))}
            </div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6 backdrop-blur md:col-span-5">
            <p className="text-xs font-bold uppercase tracking-widest text-white/40">Async by design</p>
            <h3 className="mt-1 text-lg font-bold text-white">Never blocks the candidate</h3>
            <p className="mt-2 text-sm leading-relaxed text-slate-400">
              FastAPI saves → Redis queues → Celery + LangGraph runs in the background. The candidate gets an instant success page.
            </p>
            <p className="mt-4 font-mono text-xs text-emerald-300">tasks.process_resume → COMPLETED in ~41s</p>
          </div>

          {/* three small */}
          {[
            { k: 'Public by default', v: 'No candidate passwords, JWTs or users table rows. Just a link.' },
            { k: 'Duplicate-safe', v: 'Unique (job_id, candidate_id) constraint — “You’ve already applied” is enforced in the DB.' },
            { k: 'Own your data', v: 'One company sees only its jobs. Every query is filtered by company_id.' },
          ].map((c) => (
            <div key={c.k} className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 backdrop-blur md:col-span-4">
              <h4 className="text-sm font-bold text-white">{c.k}</h4>
              <p className="mt-1 text-sm leading-relaxed text-slate-400">{c.v}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
