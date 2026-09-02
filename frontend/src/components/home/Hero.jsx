import { Link } from 'react-router-dom'

import PipelinePreview from './PipelinePreview.jsx'

export default function Hero({ heroRef, visible }) {
  return (
    <section ref={heroRef} className="relative overflow-hidden bg-slate-950">
      {/* amber/orange orbs + subtle grid with parallax */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.06)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.06)_1px,transparent_1px)] bg-[size:40px_40px]" />
        <div className="absolute -top-32 left-1/2 h-[560px] w-[900px] -translate-x-1/2 rounded-full bg-gradient-to-br from-amber-500/20 via-orange-500/20 to-rose-500/20 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-[360px] w-[360px] rounded-full bg-gradient-to-br from-amber-400/10 to-orange-400/10 blur-3xl" />
      </div>
      {/* scroll hint */}
      <div className={`absolute bottom-6 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1 transition delay-700 duration-700 ${visible ? 'opacity-100' : 'opacity-0'}`}>
        <span className="text-xs tracking-widest text-white/30">SCROLL</span>
        <span className="h-6 w-px animate-pulse bg-white/20" />
      </div>

      <div className={`relative mx-auto max-w-6xl px-4 pb-12 pt-14 sm:px-6 sm:pb-16 sm:pt-20 ${visible ? 'opacity-100' : 'opacity-0'} transition duration-700`}>
        <div className={`mx-auto max-w-3xl text-center ${visible ? 'translate-y-0 opacity-100 transition duration-700' : 'translate-y-3 opacity-0'}`}>
          <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-medium text-amber-200 backdrop-blur">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
            AI screening live — avg 41s per resume
            <span className="rounded-full bg-amber-400 px-2 py-0.5 text-[10px] font-black text-slate-900">NEW</span>
          </div>
          <h1 className="mt-5 text-4xl font-black tracking-tight text-white sm:text-5xl md:text-[56px] md:leading-[1.05]">
            Turn resumes into
            <br />
            <span className="bg-gradient-to-r from-amber-300 via-orange-400 to-rose-400 bg-clip-text text-transparent">ranked shortlists.</span>
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-slate-400 sm:text-lg">
            Publish a job, share one public link, and let
            <span className="font-semibold text-white"> RAG + LangGraph </span>
            extract, embed and score every candidate — with skills, strengths and a clear decision.
          </p>
          <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
            <Link to="/register" className="rounded-full bg-white px-7 py-3 text-sm font-bold text-slate-900 shadow-[0_8px_24px_-12px_rgba(0,0,0,0.5)] transition hover:bg-amber-50">
              Start hiring for free →
            </Link>
            <a href="#how-it-works" className="rounded-full border border-white/15 bg-white/5 px-7 py-3 text-sm font-semibold text-white backdrop-blur hover:bg-white/10">
              See how it works
            </a>
          </div>
          <p className="mt-3 text-xs text-slate-500">No candidate accounts · No credit card required</p>
        </div>

        <div className={`mt-10 sm:mt-12 ${visible ? 'translate-y-0 opacity-100 transition delay-200 duration-700' : 'translate-y-4 opacity-0'}`}>
          <PipelinePreview />
        </div>

        <div className="mt-8 flex flex-wrap items-center justify-center gap-2 text-xs">
          <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 font-medium text-slate-300">Trusted pipeline</span>
          <span className="rounded-full bg-amber-400/10 px-3 py-1 font-semibold text-amber-200 ring-1 ring-amber-400/20">Pinecone retrieval</span>
          <span className="rounded-full bg-white/5 px-3 py-1 text-slate-300 ring-1 ring-white/10">Structured LLM outputs</span>
          <span className="rounded-full bg-white/5 px-3 py-1 text-slate-300 ring-1 ring-white/10">Celery + Redis async</span>
        </div>
      </div>
    </section>
  )
}
