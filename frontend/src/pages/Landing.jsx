import { Link } from 'react-router-dom'
import ReadinessGauge from '../components/ReadinessGauge'

export default function Landing() {
  return (
    <div style={{ background: 'var(--color-bg)', minHeight: '100vh' }}>
      <header className="flex items-center justify-between" style={{ padding: '24px 48px' }}>
        <div className="flex items-center gap-2">
          <div className="sidebar-brand-mark" style={{ background: 'var(--color-accent)' }}>SG</div>
          <span style={{ fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: 18 }}>SkillGap AI</span>
        </div>
        <div className="flex gap-3">
          <Link to="/login" className="btn btn-ghost">Log in</Link>
          <Link to="/register" className="btn btn-primary">Get started</Link>
        </div>
      </header>

      <section className="flex items-center" style={{ padding: '48px', gap: 56, flexWrap: 'wrap' }}>
        <div style={{ flex: '1 1 420px', minWidth: 320 }}>
          <h1 style={{ fontSize: 42, lineHeight: 1.15, maxWidth: 520 }}>
            Discover your skill gaps.<br />Build your career roadmap.
          </h1>
          <p className="text-muted" style={{ fontSize: 16, maxWidth: 480 }}>
            SkillGap AI compares what you know against what your target job actually
            requires, then turns the gap into a phased, trackable learning plan —
            grounded in a transparent, explainable readiness score.
          </p>
          <div className="flex gap-3 mt-4">
            <Link to="/register" className="btn btn-primary">Create free account</Link>
            <Link to="/login" className="btn btn-secondary">I already have an account</Link>
          </div>
        </div>
        <div className="card flex items-center gap-4" style={{ flex: '0 0 340px' }}>
          <ReadinessGauge score={78} />
          <div>
            <div className="text-sm text-faint" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Target: DevOps Engineer
            </div>
            <div className="flex gap-2 mt-2" style={{ flexWrap: 'wrap' }}>
              <span className="badge badge-matched">8 matched</span>
              <span className="badge badge-partial">2 partial</span>
              <span className="badge badge-missing">4 missing</span>
            </div>
          </div>
        </div>
      </section>

      <section className="grid-2" style={{ padding: '0 48px 64px', maxWidth: 1000 }}>
        <div className="card">
          <h3>Transparent scoring</h3>
          <p className="text-muted text-sm">
            Every readiness score is computed from real matched, partial and missing
            skills against role requirements stored in the database — never randomized.
          </p>
        </div>
        <div className="card">
          <h3>Resume-aware</h3>
          <p className="text-muted text-sm">
            Upload a resume and SkillGap AI detects known skills automatically, letting
            you approve which ones get added to your profile.
          </p>
        </div>
      </section>
    </div>
  )
}
