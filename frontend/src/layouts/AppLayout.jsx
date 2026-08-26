import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'
import {
  IconDashboard, IconSkills, IconResume, IconAnalyze,
  IconRoadmap, IconHistory, IconProfile, IconSettings, IconLogout,
} from '../components/icons'

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: IconDashboard },
  { to: '/skills', label: 'My Skills', icon: IconSkills },
  { to: '/resume', label: 'Resume', icon: IconResume },
  { to: '/analyze', label: 'Analyze Skills', icon: IconAnalyze },
  { to: '/roadmap', label: 'Learning Roadmap', icon: IconRoadmap },
  { to: '/history', label: 'Analysis History', icon: IconHistory },
  { to: '/profile', label: 'Profile', icon: IconProfile },
  { to: '/settings', label: 'Settings', icon: IconSettings },
]

export default function AppLayout({ children, title }) {
  const { user, logout } = useAuth()
  const { showToast } = useToast()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await logout()
      showToast('You have been logged out', 'success')
      navigate('/login')
    } catch {
      showToast('Something went wrong logging out', 'error')
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-mark">SG</div>
          <div className="sidebar-brand-text">SkillGap AI</div>
        </div>
        <nav className="sidebar-nav">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
            >
              <Icon />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <button className="sidebar-link" style={{ width: '100%', background: 'transparent', border: 'none' }} onClick={handleLogout}>
            <IconLogout />
            Logout
          </button>
        </div>
      </aside>
      <div className="main-area">
        <header className="topbar">
          <h2 style={{ margin: 0 }}>{title}</h2>
          <div className="flex items-center gap-3">
            <span className="text-sm text-muted">{user?.name}</span>
          </div>
        </header>
        <main className="page-content">{children}</main>
      </div>
    </div>
  )
}
