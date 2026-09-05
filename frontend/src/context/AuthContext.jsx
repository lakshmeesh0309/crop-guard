import React, { createContext, useContext, useState, useEffect } from 'react'
import { authApi } from '../api/index.js'

const Ctx = createContext(null)

export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(() => { try { return JSON.parse(localStorage.getItem('cg_user')) } catch { return null } })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('cg_token')
    if (!token) { setLoading(false); return }
    authApi.me()
      .then(u => { setUser(u); localStorage.setItem('cg_user', JSON.stringify(u)) })
      .catch(() => { localStorage.clear(); setUser(null) })
      .finally(() => setLoading(false))
  }, [])

  async function login(email, password) {
    const d = await authApi.login({ email, password })
    localStorage.setItem('cg_token', d.access_token)
    localStorage.setItem('cg_user',  JSON.stringify(d.user))
    setUser(d.user)
    return d
  }

  async function register(payload) {
    const d = await authApi.register(payload)
    localStorage.setItem('cg_token', d.access_token)
    localStorage.setItem('cg_user',  JSON.stringify(d.user))
    setUser(d.user)
    return d
  }

  function logout() {
    localStorage.removeItem('cg_token')
    localStorage.removeItem('cg_user')
    setUser(null)
  }

  function updateUser(p) {
    const u = { ...user, ...p }
    localStorage.setItem('cg_user', JSON.stringify(u))
    setUser(u)
  }

  return <Ctx.Provider value={{ user, loading, login, register, logout, updateUser }}>{children}</Ctx.Provider>
}

export const useAuth = () => {
  const c = useContext(Ctx)
  if (!c) throw new Error('useAuth outside AuthProvider')
  return c
}
