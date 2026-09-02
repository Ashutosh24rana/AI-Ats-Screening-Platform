import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'

import { useAuth } from '../../hooks/useAuth'
import { getErrorMessage } from '../../services/api'

export default function Register() {
  const { register: registerAccount } = useAuth()
  const navigate = useNavigate()
  const [submitting, setSubmitting] = useState(false)
  const {
    register: registerField,
    handleSubmit,
    formState: { errors },
  } = useForm()

  const onSubmit = async (data) => {
    setSubmitting(true)
    try {
      await registerAccount(data)
      toast.success('Company account created!')
      navigate('/dashboard')
    } catch (error) {
      toast.error(getErrorMessage(error, 'Registration failed'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-slate-950 px-4 py-8">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[size:40px_40px]" />
        <div className="absolute -top-32 left-1/2 h-[520px] w-[800px] -translate-x-1/2 rounded-full bg-gradient-to-br from-amber-500/15 via-orange-500/15 to-rose-500/15 blur-3xl" />
      </div>
      <div className="relative w-full max-w-md">
        <div className="mb-6 text-center">
          <Link to="/" className="inline-flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-sm font-black text-slate-900">◈</span>
            <span className="text-sm font-bold tracking-tight text-white">
              talent<span className="font-light text-white/60">.ai</span>
            </span>
          </Link>
          <h1 className="mt-4 text-2xl font-black tracking-tight text-white">Create your workspace</h1>
          <p className="mt-1 text-sm text-white/50">One account owns all your jobs and candidates</p>
        </div>
        <form onSubmit={handleSubmit(onSubmit)} className="card space-y-4">
          <div>
            <label className="label" htmlFor="company_name">Company name</label>
            <input
              id="company_name"
              className="input-field"
              placeholder="Acme Inc."
              {...registerField('company_name', { required: 'Company name is required' })}
            />
            {errors.company_name && <p className="mt-1 text-xs text-rose-400">{errors.company_name.message}</p>}
          </div>
          <div>
            <label className="label" htmlFor="email">Work email</label>
            <input
              id="email"
              type="email"
              className="input-field"
              placeholder="you@acme.com"
              {...registerField('email', { required: 'Email is required' })}
            />
            {errors.email && <p className="mt-1 text-xs text-rose-400">{errors.email.message}</p>}
          </div>
          <div>
            <label className="label" htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              className="input-field"
              placeholder="At least 8 characters"
              {...registerField('password', {
                required: 'Password is required',
                minLength: { value: 8, message: 'Must be at least 8 characters' },
              })}
            />
            {errors.password && <p className="mt-1 text-xs text-rose-400">{errors.password.message}</p>}
          </div>
          <div>
            <label className="label" htmlFor="website">Website (optional)</label>
            <input id="website" className="input-field" placeholder="https://acme.com" {...registerField('website')} />
          </div>
          <div>
            <label className="label" htmlFor="description">About the company (optional)</label>
            <textarea
              id="description"
              rows={3}
              className="input-field resize-none"
              placeholder="What does your company do?"
              {...registerField('description')}
            />
          </div>
          <button type="submit" className="btn-primary w-full py-3" disabled={submitting}>
            {submitting ? 'Creating account...' : 'Create account →'}
          </button>
          <p className="text-center text-sm text-white/50">
            Already have an account?{' '}
            <Link to="/login" className="font-semibold text-amber-300 hover:text-amber-200">
              Sign in
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}
