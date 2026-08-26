import { useState } from 'react'
import AppLayout from '../layouts/AppLayout'
import ConfirmDialog from '../components/ConfirmDialog'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'
import { useNavigate } from 'react-router-dom'

export default function Settings() {
  const { user, logout } = useAuth()
  const { showToast } = useToast()
  const navigate = useNavigate()
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false)

  const handleLogout = async () => {
    await logout()
    setShowLogoutConfirm(false)
    showToast('You have been logged out', 'success')
    navigate('/login')
  }

  return (
    <AppLayout title="Settings">
      <div className="card mb-4">
        <h3>Account</h3>
        <p className="text-muted text-sm">Signed in as <strong>{user?.email}</strong></p>
        <button className="btn btn-danger mt-2" onClick={() => setShowLogoutConfirm(true)}>
          Log out
        </button>
      </div>

      <div className="card">
        <h3>About SkillGap AI</h3>
        <p className="text-muted text-sm">
          SkillGap AI is a career intelligence platform that compares your skills against
          a target job role, produces a deterministic readiness score, and builds a
          personalized learning roadmap. Scores are always calculated from your real
          skill data — never randomized.
        </p>
      </div>

      <ConfirmDialog
        open={showLogoutConfirm}
        title="Log out?"
        message="You'll need to log in again to access your dashboard."
        confirmLabel="Log out"
        onConfirm={handleLogout}
        onCancel={() => setShowLogoutConfirm(false)}
      />
    </AppLayout>
  )
}
