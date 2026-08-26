import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'

export default function Register() {
  const { register } = useAuth()
  const { showToast } = useToast()
  const navigate = useNavigate()

  const [form, setForm] = useState({ fullName: '', email: '', password: '', confirmPassword: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const update = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match')
      return
    }
    if (form.password.length < 8) {
      setError('Password must be at least 8 characters long')
      return
    }

    setSubmitting(true)
    try {
      await register(form)
      showToast('Account created — welcome to SkillGap AI', 'success')
      navigate('/dashboard', { replace: true })
    } catch (err) {
      setError(err.response?.data?.message || 'Unable to create account. Please try again.')
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
        <h1 style={{ fontSize: 22 }}>Create your account</h1>
        <p className="auth-tagline">Start mapping your path to your target role.</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="fullName">Full name</label>
            <input id="fullName" className="form-input" value={form.fullName} onChange={update('fullName')} required />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="email">Email</label>
            <input id="email" type="email" className="form-input" value={form.email} onChange={update('email')} required autoComplete="email" />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input id="password" type="password" className="form-input" value={form.password} onChange={update('password')} required autoComplete="new-password" />
            <div className="form-hint">At least 8 characters.</div>
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="confirmPassword">Confirm password</label>
            <input id="confirmPassword" type="password" className="form-input" value={form.confirmPassword} onChange={update('confirmPassword')} required autoComplete="new-password" />
          </div>
          {error && <div className="form-error mb-4">{error}</div>}
          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? 'Creating account…' : 'Create account'}
          </button>
        </form>

        <p className="text-sm text-muted mt-4">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  )
}
