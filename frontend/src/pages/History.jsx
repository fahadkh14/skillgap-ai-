import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import Skeleton from '../components/Skeleton'
import EmptyState from '../components/EmptyState'
import analysisService from '../services/analysisService'
import { useToast } from '../context/ToastContext'

export default function History() {
  const [analyses, setAnalyses] = useState([])
  const [loading, setLoading] = useState(true)
  const { showToast } = useToast()

  useEffect(() => {
    analysisService
      .listAnalyses()
      .then(setAnalyses)
      .catch(() => showToast('Could not load analysis history', 'error'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <AppLayout title="Analysis History">
      <div className="card">
        {loading ? (
          <Skeleton height={200} />
        ) : analyses.length === 0 ? (
          <EmptyState
            title="No analyses yet"
            message="Your past skill-gap analyses will appear here so you can track progress over time."
            action={<Link to="/analyze" className="btn btn-primary mt-2">Run your first analysis</Link>}
          />
        ) : (
          <table className="table">
            <thead>
              <tr><th>Target role</th><th>Score</th><th>Date</th><th></th></tr>
            </thead>
            <tbody>
              {analyses.map((a) => (
                <tr key={a.id}>
                  <td>{a.job_role_name}</td>
                  <td>{a.readiness_score}%</td>
                  <td className="text-muted">{new Date(a.created_at).toLocaleString()}</td>
                  <td><Link to={`/analysis/${a.id}`} className="btn btn-secondary btn-sm">View</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AppLayout>
  )
}
