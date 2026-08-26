import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import ReadinessGauge from '../components/ReadinessGauge'
import Skeleton from '../components/Skeleton'
import analysisService from '../services/analysisService'
import { useToast } from '../context/ToastContext'

function SkillSection({ title, badgeClass, skills, showPriority }) {
  if (skills.length === 0) return null
  return (
    <div className="card mb-4">
      <div className="card-title-row">
        <h3>{title}</h3>
        <span className={`badge ${badgeClass}`}>{skills.length}</span>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Skill</th>
            <th>Requirement</th>
            {showPriority && <th>Priority</th>}
          </tr>
        </thead>
        <tbody>
          {skills.map((s) => (
            <tr key={s.skill_name}>
              <td>{s.skill_name}</td>
              <td className="text-muted">
                {s.required ? 'Required' : 'Optional'} · min {s.minimum_proficiency}
                {s.user_proficiency ? ` · you: ${s.user_proficiency}` : ''}
              </td>
              {showPriority && (
                <td className={`priority-${(s.priority || 'low').toLowerCase()}`}>{s.priority}</td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function AnalysisDetail() {
  const { id } = useParams()
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const { showToast } = useToast()

  useEffect(() => {
    analysisService
      .getAnalysis(id)
      .then(setAnalysis)
      .catch(() => showToast('Could not load analysis', 'error'))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) {
    return (
      <AppLayout title="Skill Gap Report">
        <Skeleton height={200} />
      </AppLayout>
    )
  }

  if (!analysis) return null

  return (
    <AppLayout title="Skill Gap Report">
      <div className="card mb-4 flex items-center gap-4" style={{ flexWrap: 'wrap' }}>
        <ReadinessGauge score={analysis.readiness_score} />
        <div>
          <div className="text-faint text-sm" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            Job readiness
          </div>
          <h2>{analysis.job_role_name}</h2>
          <p className="text-muted text-sm" style={{ margin: 0 }}>
            Analyzed on {new Date(analysis.created_at).toLocaleString()}
          </p>
          <Link to="/roadmap" className="btn btn-accent btn-sm mt-2">View roadmap</Link>
        </div>
      </div>

      <SkillSection title="Matched skills" badgeClass="badge-matched" skills={analysis.matched_skills} showPriority={false} />
      <SkillSection title="Partial skills" badgeClass="badge-partial" skills={analysis.partial_skills} showPriority={true} />
      <SkillSection title="Missing skills" badgeClass="badge-missing" skills={analysis.missing_skills} showPriority={true} />
    </AppLayout>
  )
}
