import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'

import * as authService from '../services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [company, setCompany] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('ats_token')
    if (!token) {
      setLoading(false)
      return
    }
    authService
      .getMe()
      .then((data) => {
        setUser(data.user)
        setCompany(data.company)
      })
      .catch(() => {
        localStorage.removeItem('ats_token')
      })
      .finally(() => setLoading(false))
  }, [])

  const login = useCallback(async (credentials) => {
    const data = await authService.login(credentials)
    localStorage.setItem('ats_token', data.access_token)
    const me = await authService.getMe()
    setUser(me.user)
    setCompany(me.company)
    return me
  }, [])

  const register = useCallback(async (payload) => {
    const data = await authService.register(payload)
    localStorage.setItem('ats_token', data.access_token)
    const me = await authService.getMe()
    setUser(me.user)
    setCompany(me.company)
    return me
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('ats_token')
    setUser(null)
    setCompany(null)
  }, [])

  const value = useMemo(
    () => ({ user, company, loading, login, register, logout, isAuthenticated: !!user }),
    [user, company, loading, login, register, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
