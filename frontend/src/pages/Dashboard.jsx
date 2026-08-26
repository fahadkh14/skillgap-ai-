import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import ReadinessGauge from '../components/ReadinessGauge'
import Skeleton from '../components/Skeleton'
import EmptyState from '../components/EmptyState'
import dashboardService from '../services/dashboardService'
import { useToast } from '../context/ToastContext'

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const { showToast } = useToast()

  useEffect(() => {
    dashboardService
      .getDashboard()
      .then(setData)
      .catch(() => showToast('Could not load dashboard data', 'error'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <AppLayout title="Dashboard">
        <div className="stat-grid mb-4">
          {[1, 2, 3, 4].map((i) => <Skeleton key={i} height={80} />)}
        </div>
        <Skeleton height={220} />
      </AppLayout>
    )
  }

  if (!data || !data.current_target_role) {
    return (
      <AppLayout title="Dashboard">
        <div className="card">
          <EmptyState
            title="No analysis yet"
            message="Run your first skill-gap analysis to see your job readiness score, matched skills, and a personalized roadmap here."
            action={<Link to="/analyze" className="btn btn-primary mt-2">Analyze skills</Link>}
          />
        </div>
      </AppLayout>
    )
  }

  return (
    <AppLayout title="Dashboard">
      <div className="stat-grid mb-4">
        <div className="stat-card">
          <div className="stat-label">Total skills</div>
          <div className="stat-value">{data.total_skills}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Matched</div>
          <div className="stat-value" style={{ color: 'var(--color-accent)' }}>{data.matched_skills}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Partial</div>
          <div className="stat-value" style={{ color: 'var(--color-warning)' }}>{data.partial_skills}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Missing</div>
          <div className="stat-value" style={{ color: 'var(--color-danger)' }}>{data.missing_skills}</div>
        </div>
      </div>

      <div className="grid-2 mb-4">
        <div className="card flex items-center gap-4">
          <ReadinessGauge score={data.job_readiness} />
          <div>
            <div className="text-faint text-sm" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Target role
            </div>
            <h3 style={{ marginTop: 4 }}>{data.current_target_role}</h3>
            <Link to="/analyze" className="btn btn-secondary btn-sm mt-2">Re-analyze</Link>
          </div>
        </div>

        <div className="card">
          <div className="card-title-row">
            <h3>Learning progress</h3>
            <span className="text-muted text-sm">{data.learning_progress}%</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${data.learning_progress}%` }} />
          </div>
          <Link to="/roadmap" className="btn btn-secondary btn-sm mt-4">View roadmap</Link>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-title-row"><h3>Top skill gaps</h3></div>
          {data.top_skill_gaps.length === 0 ? (
            <p className="text-muted text-sm">No skill gaps — you're fully matched.</p>
          ) : (
            <table className="table">
              <thead>
                <tr><th>Skill</th><th>Priority</th></tr>
              </thead>
              <tbody>
                {data.top_skill_gaps.map((g) => (
                  <tr key={g.skill_name}>
                    <td>{g.skill_name}</td>
                    <td className={`priority-${g.priority.toLowerCase()}`}>{g.priority}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="card">
          <div className="card-title-row"><h3>Recent analyses</h3></div>
          {data.recent_analyses.length === 0 ? (
            <p className="text-muted text-sm">No analyses yet.</p>
          ) : (
            <table className="table">
              <thead>
                <tr><th>Role</th><th>Score</th><th>Date</th></tr>
              </thead>
              <tbody>
                {data.recent_analyses.map((a) => (
                  <tr key={a.id}>
                    <td>{a.job_role_name}</td>
                    <td>{a.readiness_score}%</td>
                    <td className="text-muted">{new Date(a.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </AppLayout>
  )
}
