import { createContext, useContext, useEffect, useState, useCallback } from 'react'
import authService from '../services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('skillgap_user')
    return stored ? JSON.parse(stored) : null
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('skillgap_token')
    if (!token) {
      setLoading(false)
      return
    }
    authService
      .getCurrentUser()
      .then((data) => {
        setUser(data)
        localStorage.setItem('skillgap_user', JSON.stringify(data))
      })
      .catch(() => {
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  const login = useCallback(async (credentials) => {
    const data = await authService.login(credentials)
    localStorage.setItem('skillgap_token', data.access_token)
    localStorage.setItem('skillgap_user', JSON.stringify(data.user))
    setUser(data.user)
    return data
  }, [])

  const register = useCallback(async (fields) => {
    const data = await authService.register(fields)
    localStorage.setItem('skillgap_token', data.access_token)
    localStorage.setItem('skillgap_user', JSON.stringify(data.user))
    setUser(data.user)
    return data
  }, [])

  const logout = useCallback(async () => {
    await authService.logout()
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
