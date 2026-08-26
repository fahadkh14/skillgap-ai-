import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import Skeleton from '../components/Skeleton'
import jobRoleService from '../services/jobRoleService'
import analysisService from '../services/analysisService'
import { useToast } from '../context/ToastContext'

export default function Analyze() {
  const [roles, setRoles] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedRole, setSelectedRole] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const { showToast } = useToast()
  const navigate = useNavigate()

  useEffect(() => {
    jobRoleService
      .listRoles()
      .then(setRoles)
      .catch(() => showToast('Could not load job roles', 'error'))
      .finally(() => setLoading(false))
  }, [])

  const handleAnalyze = async () => {
    if (!selectedRole) return
    setAnalyzing(true)
    try {
      const result = await analysisService.runAnalysis(selectedRole)
      showToast('Analysis complete', 'success')
      navigate(`/analysis/${result.id}`)
    } catch (err) {
      showToast(err.response?.data?.message || 'Analysis failed', 'error')
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <AppLayout title="Analyze Skills">
      <div className="card">
        <h3>Select a target job role</h3>
        <p className="text-muted text-sm">
          We'll compare your current skills against this role's requirements and calculate
          a transparent readiness score.
        </p>

        {loading ? (
          <div className="stat-grid mt-4">
            {[1, 2, 3, 4].map((i) => <Skeleton key={i} height={90} />)}
          </div>
        ) : (
          <div className="stat-grid mt-4">
            {roles.map((role) => (
              <button
                key={role.id}
                onClick={() => setSelectedRole(role.id)}
                className="card"
                style={{
                  textAlign: 'left',
                  cursor: 'pointer',
                  border: selectedRole === role.id ? '2px solid var(--color-primary)' : '1px solid var(--color-border)',
                }}
              >
                <h3 style={{ fontSize: 15 }}>{role.name}</h3>
                <p className="text-muted text-sm" style={{ margin: 0 }}>
                  {role.skills?.length || 0} required skills
                </p>
              </button>
            ))}
          </div>
        )}

        <button
          className="btn btn-primary mt-6"
          onClick={handleAnalyze}
          disabled={!selectedRole || analyzing}
        >
          {analyzing ? 'Analyzing…' : 'Run analysis'}
        </button>
      </div>
    </AppLayout>
  )
}
