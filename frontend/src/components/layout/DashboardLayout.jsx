import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

const NAV = [
  { to: '/dashboard', label: 'Overview', end: true },
  { to: '/dashboard/jobs', label: 'Jobs' },
  { to: '/dashboard/candidates', label: 'Candidates' },
]

export default function DashboardLayout() {
  const { user, company, logout } = useAuth()
  const navigate = useNavigate()
  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-[#fcfcfc]">
      {/* Header */}
      <header className="sticky top-0 z-40 h-14 border-b border-slate-200 bg-white">
        <div className="mx-auto flex h-14 max-w-[1280px] items-center justify-between px-6">
          <div className="flex items-center gap-8">
            <Link to="/dashboard" className="flex items-center gap-2">
              <span className="flex h-7 w-7 items-center justify-center rounded-md bg-slate-900 text-xs font-black text-white">◈</span>
              <span className="text-sm font-bold tracking-tight text-slate-900">
                talent<span className="font-normal text-slate-400">.ai</span>
              </span>
              <span className="rounded bg-amber-400 px-1.5 py-0.5 text-[10px] font-bold tracking-wide text-slate-900">ATS</span>
            </Link>
            <nav className="hidden items-center gap-1 md:flex">
              {NAV.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.end}
                  className={({ isActive }) =>
                    `rounded-md px-3 py-1.5 text-sm font-medium ${isActive ? 'bg-slate-900 text-white' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'}`
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden text-right md:block">
              <p className="text-sm font-medium leading-none text-slate-900">{company?.company_name}</p>
              <p className="text-xs leading-none text-slate-400">{user?.email}</p>
            </div>
            <button onClick={handleLogout} className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50">
              Log out
            </button>
          </div>
        </div>
      </header>

      {/* Mobile tabs */}
      <div className="flex border-b border-slate-200 bg-white md:hidden">
        {NAV.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            className={({ isActive }) =>
              `flex-1 border-b-2 py-3 text-center text-xs font-semibold ${isActive ? 'border-slate-900 text-slate-900' : 'border-transparent text-slate-400'}`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </div>

      {/* Content */}
      <main className="mx-auto max-w-[1280px] px-6 py-6">
        <Outlet />
      </main>
    </div>
  )
}
