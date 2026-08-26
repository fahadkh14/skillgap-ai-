import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'

export default function Login() {
  const { login } = useAuth()
  const { showToast } = useToast()
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await login({ email, password })
      showToast('Welcome back!', 'success')
      const redirectTo = location.state?.from?.pathname || '/dashboard'
      navigate(redirectTo, { replace: true })
    } catch (err) {
      setError(err.response?.data?.message || 'Unable to log in. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <div className="auth-brand">
          <div className="sidebar-brand-mark" style={{ background: 'var(--color-accent)' }}>SG</div>
          <span style={{ fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: 18 }}>SkillGap AI</span>
        </div>
        <h1 style={{ fontSize: 22 }}>Log in to your account</h1>
        <p className="auth-tagline">Discover your skill gaps. Build your career roadmap.</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>
          {error && <div className="form-error mb-4">{error}</div>}
          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? 'Logging in…' : 'Log in'}
          </button>
        </form>

        <p className="text-sm text-muted mt-4">
          Don't have an account? <Link to="/register">Create one</Link>
        </p>
        <p className="text-sm text-faint mt-2">
          Demo account: demo@skillgap.local / ChangeMe123!
        </p>
      </div>
    </div>
  )
}
