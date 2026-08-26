import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import Skeleton from '../components/Skeleton'
import EmptyState from '../components/EmptyState'
import roadmapService from '../services/roadmapService'
import { useToast } from '../context/ToastContext'

const STATUS_OPTIONS = ['Not Started', 'In Progress', 'Completed']
const PROGRESS_OPTIONS = [0, 25, 50, 75, 100]

export default function Roadmap() {
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(true)
  const [updatingSkill, setUpdatingSkill] = useState(null)
  const { showToast } = useToast()

  const load = () => {
    setLoading(true)
    roadmapService
      .getRoadmap()
      .then(setRoadmap)
      .catch(() => showToast('Could not load roadmap', 'error'))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const handleUpdate = async (skill, field, value) => {
    setUpdatingSkill(skill)
    try {
      const payload = { skill }
      payload[field] = field === 'progress' ? Number(value) : value
      const updated = await roadmapService.updateItem(roadmap.id, payload)
      setRoadmap(updated)
    } catch {
      showToast('Could not update progress', 'error')
    } finally {
      setUpdatingSkill(null)
    }
  }

  if (loading) {
    return (
      <AppLayout title="Learning Roadmap">
        <Skeleton height={300} />
      </AppLayout>
    )
  }

  if (!roadmap) {
    return (
      <AppLayout title="Learning Roadmap">
        <div className="card">
          <EmptyState
            title="No roadmap yet"
            message="Run a skill-gap analysis first — your personalized roadmap is generated from the result."
            action={<Link to="/analyze" className="btn btn-primary mt-2">Analyze skills</Link>}
          />
        </div>
      </AppLayout>
    )
  }

  return (
    <AppLayout title="Learning Roadmap">
      <div className="card mb-4">
        <div className="card-title-row">
          <div>
            <h3 style={{ marginBottom: 2 }}>{roadmap.job_role_name}</h3>
            <span className="text-muted text-sm">Overall progress</span>
          </div>
          <span className="stat-value" style={{ fontSize: 20 }}>{roadmap.overall_progress}%</span>
        </div>
        <div className="progress-track">
          <div className="progress-fill" style={{ width: `${roadmap.overall_progress}%` }} />
        </div>
      </div>

      <div className="flex-col gap-3">
        {roadmap.items.map((item, idx) => (
          <div key={item.skill} className="card">
            <div className="card-title-row" style={{ marginBottom: 8 }}>
              <div className="flex items-center gap-3">
                <span className="text-faint text-sm" style={{ fontFamily: 'var(--font-mono)' }}>
                  Phase {idx + 1}
                </span>
                <h3 style={{ margin: 0 }}>{item.skill}</h3>
                {item.priority !== 'Completed' && (
                  <span className={`priority-${item.priority.toLowerCase()} text-sm`}>{item.priority}</span>
                )}
              </div>
              <span className="text-muted text-sm">{item.estimated_duration}</span>
            </div>
            <p className="text-muted text-sm">{item.description}</p>
            {item.prerequisites?.length > 0 && (
              <p className="text-faint text-sm">Prerequisite: {item.prerequisites.join(', ')}</p>
            )}

            <div className="progress-track mt-2">
              <div className="progress-fill" style={{ width: `${item.progress}%` }} />
            </div>

            <div className="flex gap-3 mt-3" style={{ flexWrap: 'wrap' }}>
              <select
                className="form-select"
                style={{ maxWidth: 180 }}
                value={item.status}
                disabled={updatingSkill === item.skill}
                onChange={(e) => handleUpdate(item.skill, 'status', e.target.value)}
              >
                {STATUS_OPTIONS.map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
              <select
                className="form-select"
                style={{ maxWidth: 140 }}
                value={item.progress}
                disabled={updatingSkill === item.skill}
                onChange={(e) => handleUpdate(item.skill, 'progress', e.target.value)}
              >
                {PROGRESS_OPTIONS.map((p) => <option key={p} value={p}>{p}%</option>)}
              </select>
            </div>
          </div>
        ))}
      </div>
    </AppLayout>
  )
}
