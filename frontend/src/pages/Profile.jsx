import { useEffect, useState } from 'react'
import AppLayout from '../layouts/AppLayout'
import Skeleton from '../components/Skeleton'
import profileService from '../services/profileService'
import { useToast } from '../context/ToastContext'

const EXPERIENCE_LEVELS = ['Student', 'Fresher', 'Junior', 'Mid-Level', 'Senior']

export default function Profile() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const { showToast } = useToast()

  useEffect(() => {
    profileService
      .getProfile()
      .then(setProfile)
      .catch(() => showToast('Could not load profile', 'error'))
      .finally(() => setLoading(false))
  }, [])

  const update = (field) => (e) => setProfile((p) => ({ ...p, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      const updated = await profileService.updateProfile({
        full_name: profile.full_name,
        phone: profile.phone,
        college: profile.college,
        education: profile.education,
        graduation_year: profile.graduation_year ? Number(profile.graduation_year) : null,
        experience_level: profile.experience_level,
        current_role: profile.current_role,
        target_role: profile.target_role,
        bio: profile.bio,
      })
      setProfile(updated)
      showToast('Profile updated', 'success')
    } catch (err) {
      showToast(err.response?.data?.message || 'Could not save profile', 'error')
    } finally {
      setSaving(false)
    }
  }

  if (loading || !profile) {
    return (
      <AppLayout title="Profile">
        <Skeleton height={400} />
      </AppLayout>
    )
  }

  return (
    <AppLayout title="Profile">
      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Full name</label>
              <input className="form-input" value={profile.full_name || ''} onChange={update('full_name')} required />
            </div>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input className="form-input" value={profile.email || ''} disabled />
            </div>
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Phone</label>
              <input className="form-input" value={profile.phone || ''} onChange={update('phone')} />
            </div>
            <div className="form-group">
              <label className="form-label">College</label>
              <input className="form-input" value={profile.college || ''} onChange={update('college')} />
            </div>
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Education</label>
              <input className="form-input" value={profile.education || ''} onChange={update('education')} placeholder="e.g. BCA" />
            </div>
            <div className="form-group">
              <label className="form-label">Graduation year</label>
              <input type="number" className="form-input" value={profile.graduation_year || ''} onChange={update('graduation_year')} />
            </div>
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Experience level</label>
              <select className="form-select" value={profile.experience_level || 'Student'} onChange={update('experience_level')}>
                {EXPERIENCE_LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Current role</label>
              <input className="form-input" value={profile.current_role || ''} onChange={update('current_role')} />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Target role</label>
            <input className="form-input" value={profile.target_role || ''} onChange={update('target_role')} placeholder="e.g. DevOps Engineer" />
          </div>

          <div className="form-group">
            <label className="form-label">Bio</label>
            <textarea className="form-textarea" rows={4} value={profile.bio || ''} onChange={update('bio')} />
          </div>

          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? 'Saving…' : 'Save profile'}
          </button>
        </form>
      </div>
    </AppLayout>
  )
}
