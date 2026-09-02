import { Link } from 'react-router-dom'

import { useAuth } from '../../hooks/useAuth'

export default function HomeNavbar() {
  const { isAuthenticated } = useAuth()
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/70 backdrop-blur-xl">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
        <Link to="/" className="flex items-center gap-2.5">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-sm font-black text-slate-900">◈</span>
          <span className="text-[15px] font-bold tracking-tight text-white">
            talent<span className="font-light text-white/60">.ai</span>
          </span>
          <span className="hidden rounded-full bg-amber-400 px-2 py-0.5 text-[10px] font-black tracking-widest text-slate-900 sm:inline">ATS</span>
        </Link>
        <nav className="flex items-center gap-1 sm:gap-2">
          <a href="#how-it-works" className="hidden rounded-full px-3 py-1.5 text-sm font-medium text-white/60 hover:bg-white/5 hover:text-white sm:block">
            How it works
          </a>
          <a href="#features" className="hidden rounded-full px-3 py-1.5 text-sm font-medium text-white/60 hover:bg-white/5 hover:text-white sm:block">
            Features
          </a>
          {isAuthenticated ? (
            <Link to="/dashboard" className="ml-2 rounded-full bg-white px-4 py-2 text-sm font-bold text-slate-900 shadow-sm transition hover:bg-amber-50">
              Dashboard →
            </Link>
          ) : (
            <>
              <Link to="/login" className="rounded-full px-4 py-2 text-sm font-medium text-white/70 hover:text-white">
                Sign in
              </Link>
              <Link to="/register" className="rounded-full bg-white px-4 py-2 text-sm font-bold text-slate-900 shadow-sm transition hover:bg-amber-50">
                Start hiring
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
