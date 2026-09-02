export default function StepCard({ step, index, visible, isLast }) {
  return (
    <div
      className={`relative flex gap-4 transition-all duration-700 md:gap-6 ${visible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}`}
      style={{ transitionDelay: `${index * 110}ms` }}
    >
      {/* line */}
      <div className="relative flex flex-col items-center">
        <div
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full border bg-slate-900 text-sm shadow-sm transition duration-500 ${visible ? 'border-amber-400/30 bg-amber-400/10 text-amber-300' : 'border-white/10 text-white/30'}`}
        >
          {step.icon}
        </div>
        {!isLast && <div className={`mt-2 w-px flex-1 bg-gradient-to-b from-amber-400/40 to-white/5 transition duration-700 ${visible ? 'opacity-100' : 'opacity-0'}`} style={{ transitionDelay: `${index * 110 + 300}ms` }} />}
      </div>

      <div
        className={`group flex-1 rounded-2xl border p-5 shadow-sm backdrop-blur transition hover:-translate-y-0.5 hover:shadow-md ${visible ? 'border-white/10 bg-white/[0.04] hover:bg-white/[0.06] hover:border-amber-400/20' : 'border-transparent bg-transparent'}`}
      >
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-amber-400 px-2 py-0.5 text-xs font-black text-slate-900">{step.n}</span>
          <h3 className="text-sm font-semibold text-white">{step.title}</h3>
        </div>
        <p className="mt-2 text-sm leading-relaxed text-slate-400">{step.desc}</p>
      </div>
    </div>
  )
}
