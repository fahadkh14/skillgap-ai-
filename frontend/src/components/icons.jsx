const stroke = { fill: 'none', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round', strokeLinejoin: 'round' }

export function IconDashboard(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <rect x="3" y="3" width="8" height="8" rx="1.5" {...stroke} />
      <rect x="13" y="3" width="8" height="5" rx="1.5" {...stroke} />
      <rect x="13" y="10" width="8" height="11" rx="1.5" {...stroke} />
      <rect x="3" y="13" width="8" height="8" rx="1.5" {...stroke} />
    </svg>
  )
}

export function IconSkills(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <path d="M12 3l2.5 5.2 5.7.8-4.1 4 1 5.7-5.1-2.7-5.1 2.7 1-5.7-4.1-4 5.7-.8L12 3z" {...stroke} />
    </svg>
  )
}

export function IconResume(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <path d="M7 3h7l4 4v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z" {...stroke} />
      <path d="M14 3v4h4" {...stroke} />
      <path d="M8 12h8M8 15.5h8M8 18.5h5" {...stroke} />
    </svg>
  )
}

export function IconAnalyze(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <circle cx="11" cy="11" r="7" {...stroke} />
      <path d="M20 20l-4.3-4.3" {...stroke} />
    </svg>
  )
}

export function IconRoadmap(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <path d="M4 19c3-6 6 6 9-6 1.5-4.5 4-6 7-6" {...stroke} />
      <circle cx="4" cy="19" r="1.4" fill="currentColor" stroke="none" />
      <circle cx="20" cy="7" r="1.4" fill="currentColor" stroke="none" />
    </svg>
  )
}

export function IconHistory(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <circle cx="12" cy="12" r="8" {...stroke} />
      <path d="M12 7.5V12l3 2" {...stroke} />
    </svg>
  )
}

export function IconProfile(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <circle cx="12" cy="8" r="3.5" {...stroke} />
      <path d="M4.5 20c1.6-3.6 5-5.2 7.5-5.2s5.9 1.6 7.5 5.2" {...stroke} />
    </svg>
  )
}

export function IconSettings(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <circle cx="12" cy="12" r="3" {...stroke} />
      <path d="M19.4 13.5a7.7 7.7 0 0 0 0-3l2-1.4-2-3.4-2.3.9a7.6 7.6 0 0 0-2.6-1.5L14 2.5h-4l-.5 2.6a7.6 7.6 0 0 0-2.6 1.5l-2.3-.9-2 3.4 2 1.4a7.7 7.7 0 0 0 0 3l-2 1.4 2 3.4 2.3-.9c.76.66 1.65 1.17 2.6 1.5l.5 2.6h4l.5-2.6a7.6 7.6 0 0 0 2.6-1.5l2.3.9 2-3.4-2-1.4z" {...stroke} />
    </svg>
  )
}

export function IconLogout(props) {
  return (
    <svg viewBox="0 0 24 24" className="sidebar-icon" {...props}>
      <path d="M9 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h3" {...stroke} />
      <path d="M15 16l4-4-4-4" {...stroke} />
      <path d="M19 12H9" {...stroke} />
    </svg>
  )
}
