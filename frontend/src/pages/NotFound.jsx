import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="auth-shell">
      <div className="auth-card" style={{ textAlign: 'center' }}>
        <h1 style={{ fontSize: 48 }}>404</h1>
        <p className="text-muted">This page doesn't exist.</p>
        <Link to="/dashboard" className="btn btn-primary mt-4">Back to dashboard</Link>
      </div>
    </div>
  )
}
