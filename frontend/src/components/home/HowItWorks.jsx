import { Link } from 'react-router-dom'

import StepCard from './StepCard.jsx'

const STEPS = [
  {
    n: '01',
    title: 'Company registers',
    desc: 'One company account owns everything — jobs, applications and scores. No candidate logins, ever.',
    icon: '◈',
  },
  {
    n: '02',
    title: 'Create & publish a job',
    desc: 'Title, description, required & preferred skills, experience and location. Publish to generate the public link.',
    icon: '✦',
  },
  {
    n: '03',
    title: 'Share the public link',
    desc: 'Every job gets a unique Link. Post it on LinkedIn, your site, or email — anyone can apply.',
    icon: '↗',
  },
  {
    n: '04',
    title: 'Candidate applies — no account',
    desc: 'Name, email, phone and a PDF resume. We validate the file, block duplicates and queue the AI job.',
    icon: '⬣',
  },
  {
    n: '05',
    title: 'AI extracts, embeds & retrieves',
    desc: 'PyPDF → chunk → Gemini embeddings → Pinecone (metadata-filtered). Then a job-aware RAG query pulls the top excerpts.',
    icon: '⬡',
  },
  {
    n: '06',
    title: 'LangGraph scores & decides',
    desc: 'Five structured evaluations (skill, experience, semantic, ATS, summary) → weighted final score → SHORTLISTED / REVIEW / REJECTED.',
    icon: '✧',
  },
]

export default function HowItWorks({ stepsRef, visible }) {
  return (
    <section id="how-it-works" ref={stepsRef} className="relative overflow-hidden border-y border-white/5 bg-slate-900 py-16 sm:py-20">
      <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[size:40px_40px]" />
      <div className="absolute left-1/2 top-0 h-[420px] w-[720px] -translate-x-1/2 rounded-full bg-gradient-to-br from-amber-500/10 via-orange-500/10 to-rose-500/10 blur-3xl" />
      <div className="relative mx-auto max-w-6xl px-4 sm:px-6">
        <div className={`mx-auto max-w-2xl text-center transition duration-700 ${visible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
          <p className="text-xs font-bold uppercase tracking-widest text-amber-300">Pipeline</p>
          <h2 className="mt-2 text-2xl font-black tracking-tight text-white sm:text-3xl">Six steps. One shortlist.</h2>
          <p className="mx-auto mt-2 max-w-xl text-sm leading-relaxed text-slate-400">
            Staggered on scroll — each step lights up as you go. The candidate sees a simple form; you see a ranked pipeline.
          </p>
        </div>
        <div className="mx-auto mt-10 grid max-w-3xl gap-3">
          {STEPS.map((step, i) => (
            <div
              key={step.n}
              className={`transition-all duration-700 ${visible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}`}
              style={{ transitionDelay: `${i * 120}ms` }}
            >
              <StepCard step={step} index={i} visible={visible} isLast={i === STEPS.length - 1} />
            </div>
          ))}
        </div>
        <div className={`mt-10 flex justify-center transition delay-[700ms] duration-700 ${visible ? 'opacity-100' : 'opacity-0'}`}>
          <Link to="/register" className="rounded-full bg-white px-7 py-3 text-sm font-bold text-slate-900 shadow hover:bg-amber-50">
            Publish your first job →
          </Link>
        </div>
      </div>
    </section>
  )
}
