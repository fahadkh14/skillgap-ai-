import { useEffect, useState } from 'react'
import AppLayout from '../layouts/AppLayout'
import EmptyState from '../components/EmptyState'
import Skeleton from '../components/Skeleton'
import ConfirmDialog from '../components/ConfirmDialog'
import skillService from '../services/skillService'
import { useToast } from '../context/ToastContext'

const PROFICIENCIES = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

export default function Skills() {
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [profFilter, setProfFilter] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [form, setForm] = useState({ skill_name: '', proficiency: 'Beginner', years_of_experience: '' })
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const { showToast } = useToast()

  const load = () => {
    setLoading(true)
    skillService
      .listSkills({ search, proficiency: profFilter })
      .then(setSkills)
      .catch(() => showToast('Could not load skills', 'error'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    const t = setTimeout(load, 250)
    return () => clearTimeout(t)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search, profFilter])

  const resetForm = () => {
    setForm({ skill_name: '', proficiency: 'Beginner', years_of_experience: '' })
    setEditingId(null)
    setShowForm(false)
  }

  const startEdit = (skill) => {
    setForm({ skill_name: skill.skill_name, proficiency: skill.proficiency, years_of_experience: skill.years_of_experience })
    setEditingId(skill.id)
    setShowForm(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      if (editingId) {
        await skillService.updateSkill(editingId, {
          proficiency: form.proficiency,
          years_of_experience: Number(form.years_of_experience) || 0,
        })
        showToast('Skill updated', 'success')
      } else {
        await skillService.addSkill({
          skill_name: form.skill_name,
          proficiency: form.proficiency,
          years_of_experience: Number(form.years_of_experience) || 0,
        })
        showToast('Skill added', 'success')
      }
      resetForm()
      load()
    } catch (err) {
      showToast(err.response?.data?.message || 'Could not save skill', 'error')
    } finally {
      setSubmitting(false)
    }
  }

  const confirmDelete = async () => {
    try {
      await skillService.deleteSkill(deleteTarget.id)
      showToast('Skill removed', 'success')
      setDeleteTarget(null)
      load()
    } catch {
      showToast('Could not remove skill', 'error')
    }
  }

  return (
    <AppLayout title="My Skills">
      <div className="card mb-4">
        <div className="flex gap-3" style={{ flexWrap: 'wrap' }}>
          <input
            className="form-input"
            placeholder="Search skills…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ maxWidth: 260 }}
          />
          <select className="form-select" value={profFilter} onChange={(e) => setProfFilter(e.target.value)} style={{ maxWidth: 200 }}>
            <option value="">All proficiencies</option>
            {PROFICIENCIES.map((p) => <option key={p} value={p}>{p}</option>)}
          </select>
          <button className="btn btn-primary" style={{ marginLeft: 'auto' }} onClick={() => { resetForm(); setShowForm(true) }}>
            + Add skill
          </button>
        </div>
      </div>

      {showForm && (
        <div className="card mb-4">
          <h3>{editingId ? 'Edit skill' : 'Add a skill'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Skill name</label>
                <input
                  className="form-input"
                  value={form.skill_name}
                  onChange={(e) => setForm((f) => ({ ...f, skill_name: e.target.value }))}
                  disabled={!!editingId}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Proficiency</label>
                <select
                  className="form-select"
                  value={form.proficiency}
                  onChange={(e) => setForm((f) => ({ ...f, proficiency: e.target.value }))}
                >
                  {PROFICIENCIES.map((p) => <option key={p} value={p}>{p}</option>)}
                </select>
              </div>
            </div>
            <div className="form-group" style={{ maxWidth: 200 }}>
              <label className="form-label">Years of experience</label>
              <input
                type="number"
                min="0"
                step="0.5"
                className="form-input"
                value={form.years_of_experience}
                onChange={(e) => setForm((f) => ({ ...f, years_of_experience: e.target.value }))}
                required
              />
            </div>
            <div className="flex gap-3">
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? 'Saving…' : editingId ? 'Save changes' : 'Add skill'}
              </button>
              <button type="button" className="btn btn-secondary" onClick={resetForm}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="card">
        {loading ? (
          <div className="flex-col gap-2">
            {[1, 2, 3].map((i) => <Skeleton key={i} height={40} />)}
          </div>
        ) : skills.length === 0 ? (
          <EmptyState
            title="No skills yet"
            message="Add skills manually or upload your resume to detect them automatically."
          />
        ) : (
          <table className="table">
            <thead>
              <tr><th>Skill</th><th>Proficiency</th><th>Experience</th><th></th></tr>
            </thead>
            <tbody>
              {skills.map((s) => (
                <tr key={s.id}>
                  <td>{s.skill_name}</td>
                  <td><span className="badge badge-neutral">{s.proficiency}</span></td>
                  <td className="text-muted">{s.years_of_experience} yrs</td>
                  <td>
                    <div className="flex gap-2">
                      <button className="btn btn-secondary btn-sm" onClick={() => startEdit(s)}>Edit</button>
                      <button className="btn btn-danger btn-sm" onClick={() => setDeleteTarget(s)}>Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <ConfirmDialog
        open={!!deleteTarget}
        title="Remove this skill?"
        message={`This will remove "${deleteTarget?.skill_name}" from your profile.`}
        confirmLabel="Delete"
        onConfirm={confirmDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </AppLayout>
  )
}
